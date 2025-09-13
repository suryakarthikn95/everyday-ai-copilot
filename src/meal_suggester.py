import json
import os
from typing import List, Dict, Any

DATA_PATH = os.path.join(os.path.dirname(__file__), "..", "data", "recipes.json")

# Simple synonym map so user inputs still match dataset
SYNONYMS = {
    "capsicum": "bell pepper",
    "garbanzo": "chickpeas",
    "chickpea": "chickpeas",
    "curd": "yogurt",
    "cilantro": "coriander",
    "green onion": "spring onion",
    "scallion": "spring onion",
    "maida": "all-purpose flour",
    "attā": "whole wheat flour"
}

# Pantry items that shouldn't penalize if missing (can be overridden from UI)
PANTRY_DEFAULT = {"salt", "pepper", "oil", "olive oil", "water"}

def canon(item: str) -> str:
    t = item.strip().lower()
    return SYNONYMS.get(t, t)

def load_recipes() -> List[Dict[str, Any]]:
    with open(DATA_PATH, "r", encoding="utf-8") as f:
        return json.load(f)

def score_recipe(user_ings: List[str], recipe_ings: List[str], pantry: set) -> Dict[str, Any]:
    user = {canon(i) for i in user_ings if i.strip()}
    recipe = [canon(i) for i in recipe_ings]

    match = [i for i in recipe if i in user]
    missing_all = [i for i in recipe if i not in user]
    # Don't penalize pantry items
    missing_non_pantry = [i for i in missing_all if i not in pantry]

    # Heuristic:
    # - reward exact matches heavily
    # - lightly reward overall coverage
    # - penalize non-pantry missing items
    coverage = len(match) / max(1, len(recipe))
    score = (len(match) * 2.0) + coverage - (len(missing_non_pantry) * 1.2)

    return {
        "score": score,
        "match": match,
        "missing": missing_all,
        "missing_non_pantry": missing_non_pantry
    }

def suggest_meals(
    ingredients: List[str],
    top_k: int = 5,
    max_time: int = 0,
    pantry_items: List[str] | None = None
) -> List[Dict[str, Any]]:
    recipes = load_recipes()
    pantry = {canon(p) for p in (pantry_items or PANTRY_DEFAULT)}

    ranked = []
    for r in recipes:
        if max_time and r.get("time_min", 10**9) > max_time:
            continue
        s = score_recipe(ingredients, r["ingredients"], pantry)
        ranked.append({
            "title": r["title"],
            "time_min": r["time_min"],
            "tags": r.get("tags", []),
            "steps": r.get("steps", []),
            "match": s["match"],
            "missing": s["missing"],
            "missing_non_pantry": s["missing_non_pantry"],
            "score": s["score"]
        })

    # Sort: best score first, then faster recipes
    ranked.sort(key=lambda x: (-x["score"], x["time_min"]))
    return ranked[:top_k]