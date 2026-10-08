import os
import json
import subprocess
import pytest

# Dynamically locate the project root directory
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SKILLS_DIR = os.path.join(BASE_DIR, "skills", "nutrilens-auditor", "scripts")

MACRO_VERIFIER_PATH = os.path.join(SKILLS_DIR, "macro_verifier.py")
ALLERGEN_SCANNER_PATH = os.path.join(SKILLS_DIR, "allergen_scanner.py")


def run_skill_script(script_path: str, input_data: dict) -> dict:
    """
    Executes a skill CLI script by piping JSON into stdin
    and parsing the resulting output from stdout.
    """
    if not os.path.exists(script_path):
        pytest.fail(f"Script file not found at expected path: {script_path}")

    process = subprocess.Popen(
        ["python", script_path],
        stdin=subprocess.PIPE,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True
    )
    stdout, stderr = process.communicate(input=json.dumps(input_data))

    if process.returncode != 0:
        raise RuntimeError(f"Script execution failed with error:\n{stderr}")

    return json.loads(stdout)


def test_atwater_calorie_calculation():
    """
    Tests the Atwater 4:4:9 system calculation:
    - Protein: 20g * 4 = 80 kcal
    - Net Carbs: (20g - 2g fiber) * 4 = 72 kcal
    - Fiber: 2g * 2 = 4 kcal
    - Fat: 4g * 9 = 36 kcal
    - Expected Total = 192.0 kcal
    """
    mock_input = {
        "calories": 200.0,
        "protein_g": 20.0,
        "carbs_g": 20.0,
        "fiber_g": 2.0,
        "fat_g": 4.0,
        "ingredients": ["Whey Protein Concentrate", "Cocoa Powder", "Stevia"]
    }

    report = run_skill_script(MACRO_VERIFIER_PATH, mock_input)

    assert report["calculated_calories"] == 192.0
    assert report["declared_calories"] == 200.0
    assert report["variance_percentage"] == 4.2
    assert len(report["deceptive_ingredients"]) == 0
    assert report["passed"] is True


def test_deceptive_filler_detection():
    """
    Ensures high-GI additives like Maltodextrin and Dextrose are 
    detected and cause the audit score to drop.
    """
    mock_input = {
        "calories": 150.0,
        "protein_g": 10.0,
        "carbs_g": 20.0,
        "fiber_g": 0.0,
        "fat_g": 3.0,
        "ingredients": ["Maltodextrin", "Soy Protein Isolate", "Dextrose"]
    }

    report = run_skill_script(MACRO_VERIFIER_PATH, mock_input)

    # Extract flagged ingredient names
    flagged_names = [item["ingredient"] for item in report["deceptive_ingredients"]]

    assert "maltodextrin" in flagged_names
    assert "dextrose" in flagged_names
    assert report["integrity_score"] <= 60
    assert report["passed"] is False


def test_allergen_scanner_cross_referencing():
    """
    Tests that common allergens are correctly cross-referenced 
    from the ingredient list.
    """
    mock_input = {
        "ingredients": [
            "Peanut Butter",
            "Whey Protein (Milk)",
            "Soy Lecithin",
            "Rolled Oats"
        ]
    }

    report = run_skill_script(ALLERGEN_SCANNER_PATH, mock_input)

    detected = report["detected_allergens"]
    assert "peanuts" in detected
    assert "milk" in detected
    assert "soy" in detected
    assert "wheat" not in detected