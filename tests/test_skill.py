import subprocess
import json
import os

def test_macro_verifier_atwater():
    mock_data = {
        "calories": 200.0,
        "protein_g": 20.0,
        "carbs_g": 20.0,
        "fiber_g": 0.0,
        "fat_g": 4.4,
        "ingredients": ["Whey protein", "Maltodextrin"]
    }
    script = os.path.join("skills", "nutrilens-auditor", "scripts", "macro_verifier.py")
    proc = subprocess.Popen(["python", script], stdin=subprocess.PIPE, stdout=subprocess.PIPE, text=True)
    stdout, _ = proc.communicate(input=json.dumps(mock_data))
    res = json.loads(stdout)

    assert "calculated_calories" in res
    assert "maltodextrin" in res["deceptive_ingredients"]
    assert res["integrity_score"] < 100