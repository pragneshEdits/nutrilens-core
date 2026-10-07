import os
import json
import base64
import requests
from PIL import Image
from pydantic import BaseModel, Field
from google import genai
from google.genai import types
from dotenv import load_dotenv

load_dotenv()

class ExtractedNutrition(BaseModel):
    calories: float = Field(default=0.0)
    protein_g: float = Field(default=0.0)
    carbs_g: float = Field(default=0.0)
    fiber_g: float = Field(default=0.0)
    fat_g: float = Field(default=0.0)
    ingredients: list[str] = Field(default_factory=list)

class InferenceEngine:
    def __init__(self):
        self.api_key = os.getenv("GEMINI_API_KEY")
        self.client = genai.Client(api_key=self.api_key) if self.api_key else None

    def extract_local_ollama(self, image_path: str) -> dict:
        """Runs offline on RTX 3050 (6GB VRAM) via Ollama."""
        with open(image_path, "rb") as f:
            b64_img = base64.b64encode(f.read()).decode("utf-8")

        prompt = (
            "Extract nutritional values and ingredients. "
            "Return valid JSON matching keys: calories, protein_g, carbs_g, fiber_g, fat_g, ingredients (as array of strings)."
        )
        res = requests.post(
            "http://localhost:11434/api/generate",
            json={
                "model": "gemma",
                "prompt": prompt,
                "images": [b64_img],
                "format": "json",
                "stream": False
            },
            timeout=25
        )
        return json.loads(res.json()["response"])

    def extract_cloud_gemini(self, image_path: str) -> dict:
        """Calls Gemma 4 on the Gemini API."""
        if not self.client:
            raise ValueError("GEMINI_API_KEY is not set.")
        
        img = Image.open(image_path)
        prompt = "Extract nutritional metrics and full ingredient list into structured schema."
        response = self.client.models.generate_content(
            model="gemma-4-31b-it",
            contents=[prompt, img],
            config=types.GenerateContentConfig(
                response_mime_type="application/json",
                response_schema=ExtractedNutrition,
                temperature=0.1
            )
        )
        return json.loads(response.text)

    def process(self, image_path: str, force_cloud: bool = False) -> dict:
        if not force_cloud:
            try:
                print("⚡ [Edge] Processing locally on RTX 3050...")
                return self.extract_local_ollama(image_path)
            except Exception as e:
                print(f"⚠️ [Edge Fallback] Local inference failed ({e}). Escalating to Cloud...")
        
        print("☁️ [Cloud] Processing via Gemini API (Gemma 4)...")
        return self.extract_cloud_gemini(image_path)