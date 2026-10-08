"""
NutriLens Test Fixtures Module.

Contains sample packaging images and pre-cached OCR extractions
for offline testing, automated tests, and backup demo presentations.
"""

import os
import json

FIXTURES_DIR = os.path.dirname(os.path.abspath(__file__))
MOCK_LABELS_PATH = os.path.join(FIXTURES_DIR, "mock_labels.json")

def load_mock_labels() -> dict:
    """Loads pre-cached mock nutritional extraction data."""
    if os.path.exists(MOCK_LABELS_PATH):
        with open(MOCK_LABELS_PATH, "r", encoding="utf-8") as f:
            return json.load(f)
    return {}