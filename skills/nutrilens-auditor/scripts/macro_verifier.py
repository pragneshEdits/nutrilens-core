import sys
import json
import os

def verify(data: dict) -> dict:
    declared_cals = float(data.get("calories", 0.0))
    p = float(data.get("protein_g", 0.0))
    c = float(data.get("carbs_g", 0.0))
    f = float(data.get("fat_g", 0.0))
    fiber = float(data.get("fiber_g", 0.0))

    # Atwater factor math: 4:4:9 system (2 kcal/g for dietary fiber)
    net_carbs = max(0.0, c - fiber)
    calculated_cals = round((p * 4.0) + (net_carbs * 4.0) + (fiber * 2.0) + (f * 9.0), 1)
    
    variance = round(abs(declared_cals - calculated_cals) / calculated_cals * 100, 1) if calculated_cals > 0 else 0.0

    # Load reference glycemic database
    ref_path = os.path.join(os.path.dirname(__file__), "..", "references", "glycemic_index.json")
    deceptive_found = []
    
    if os.path.exists(ref_path):
        with open(ref_path, "r") as ref_file:
            gi_db = json.load(ref_file)
            ingredients_str = " ".join(data.get("ingredients", [])).lower()
            for additive, meta in gi_db.items():
                if additive in ingredients_str:
                    deceptive_found.append({"ingredient": additive, "gi": meta["gi"], "risk": meta["risk"]})

    # Integrity score computation (100 base)
    score = max(0, int(100 - (variance * 1.2) - (len(deceptive_found) * 20)))

    return {
        "calculated_calories": calculated_cals,
        "declared_calories": declared_cals,
        "variance_percentage": variance,
        "deceptive_ingredients": deceptive_found,
        "integrity_score": score,
        "passed": variance <= 15.0 and len(deceptive_found) == 0
    }

if __name__ == "__main__":
    raw = sys.stdin.read()
    payload = json.loads(raw) if raw.strip() else {}
    print(json.dumps(verify(payload), indent=2))