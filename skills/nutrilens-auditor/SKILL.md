---
name: nutrilens-auditor
description: Audits nutritional labels and packaging claims using multimodal Gemma 4. Deterministically verifies Atwater caloric math, identifies hidden high-GI sweeteners like maltodextrin, and scores claim integrity.
license: Apache-2.0
metadata:
  version: "1.0.0"
  standard: "agentskills.io"
---

# NutriLens Food Auditor Skill

## Operational Pipeline
1. Extract numerical nutrition tables, front claims, and ingredients from food packaging using multimodal Gemma 4.
2. Pipe extracted JSON into `scripts/macro_verifier.py`.
3. Check additive Glycemic Index against `references/glycemic_index.json`.
4. Cross-reference potential allergens against `scripts/allergen_scanner.py`.
5. Output verified audit report containing the Claim Integrity Score.