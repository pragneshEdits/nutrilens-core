import os
from PIL import Image, ImageDraw, ImageFont

def draw_label(title: str, calories: str, protein: str, carbs: str, fat: str, ingredients: str, output_path: str):
    # Create a white background image (400x550)
    img = Image.new("RGB", (400, 550), color=(255, 255, 255))
    draw = ImageDraw.Draw(img)

    # Outer border
    draw.rectangle([10, 10, 390, 540], outline=(0, 0, 0), width=3)
    
    # Header
    draw.text((20, 20), title, fill=(0, 0, 0))
    draw.text((20, 45), "Nutrition Facts", fill=(0, 0, 0))
    draw.line([20, 70, 380, 70], fill=(0, 0, 0), width=4)

    # Caloric & Macro Details
    draw.text((20, 80), f"Amount Per Serving", fill=(0, 0, 0))
    draw.text((20, 100), f"Calories {calories}", fill=(0, 0, 0))
    draw.line([20, 125, 380, 125], fill=(0, 0, 0), width=2)

    draw.text((20, 135), f"Total Fat {fat}g", fill=(0, 0, 0))
    draw.text((20, 160), f"Total Carbohydrate {carbs}g", fill=(0, 0, 0))
    draw.text((20, 185), f"Protein {protein}g", fill=(0, 0, 0))
    draw.line([20, 215, 380, 215], fill=(0, 0, 0), width=4)

    # Ingredients Section
    draw.text((20, 230), "INGREDIENTS:", fill=(0, 0, 0))
    
    # Simple word wrapper for ingredients text
    words = ingredients.split(" ")
    lines = []
    current_line = ""
    for word in words:
        if len(current_line + word) < 40:
            current_line += word + " "
        else:
            lines.append(current_line)
            current_line = word + " "
    lines.append(current_line)

    y_offset = 255
    for line in lines:
        draw.text((20, y_offset), line, fill=(0, 0, 0))
        y_offset += 22

    img.save(output_path)
    print(f"✅ Generated sample label: {output_path}")

if __name__ == "__main__":
    base_dir = os.path.dirname(os.path.abspath(__file__))

    # 1. Clean Label
    draw_label(
        title="PureFit Whey Bar (Clean Label)",
        calories="220",
        protein="20",
        carbs="18",
        fat="6",
        ingredients="Whey Protein Isolate, Almond Butter, Chicory Root Fiber, Stevia Extract.",
        output_path=os.path.join(base_dir, "clean_protein_bar.jpg")
    )

    # 2. Deceptive Label (Maltodextrin / Calorie Mismatch)
    draw_label(
        title="Keto Crunch Bar (Deceptive Label)",
        calories="180",
        protein="15",
        carbs="22",
        fat="4",
        ingredients="Whey Protein Concentrate, Maltodextrin, Palm Kernel Oil, Dextrose, Artificial Flavors.",
        output_path=os.path.join(base_dir, "deceptive_maltodextrin_snack.jpg")
    )