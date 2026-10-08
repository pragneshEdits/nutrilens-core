import sys
import json

COMMON_ALLERGENS = ["peanuts", "tree nuts", "milk", "eggs", "soy", "wheat", "fish", "shellfish", "sesame"]

def scan_allergens(ingredients: list) -> list:
    ingredients_str = " ".join(ingredients).lower()
    detected = [allergen for allergen in COMMON_ALLERGENS if allergen in ingredients_str]
    return detected

if __name__ == "__main__":
    raw = sys.stdin.read()
    payload = json.loads(raw) if raw.strip() else {}
    detected = scan_allergens(payload.get("ingredients", []))
    print(json.dumps({"detected_allergens": detected}))