import os
import streamlit as st

# --- Imports from your codebase ---
from src.meal_suggester import suggest_meals, load_recipes, DATA_PATH
from src.nlp import parse_ingredients

# --- Page setup ---
st.set_page_config(page_title="Everyday AI Copilot — Meals", page_icon="🍳")
st.title("🍳 Everyday AI Copilot — Meal Suggestions")

st.write("Type naturally (e.g., *I have leftover rice, half an onion, some spinach*) or a comma-separated list.")

# --- Quick health/debug panel (you can hide later) ---
with st.expander("Debug (click to open)"):
    st.write("Working directory:", os.getcwd())
    st.write("Recipe file path:", DATA_PATH)
    st.write("Recipe file exists:", os.path.exists(DATA_PATH))
    try:
        _recipes = load_recipes()
        st.write("Recipes loaded:", len(_recipes))
    except Exception as e:
        st.error(f"Failed to load recipes: {e}")

# --- Inputs ---
ingredients_text = st.text_input(
    "What do you have?",
    value="I have leftover rice, half an onion and some spinach."
)
use_ai = st.checkbox("Use AI to parse ingredients (recommended)", value=True)

col1, col2, col3 = st.columns([1, 1, 2])
with col1:
    top_k = st.slider("How many suggestions?", 1, 10, 5)
with col2:
    max_time = st.slider("Max time (min)", 0, 60, 0, help="0 = no limit")
with col3:
    pantry_text = st.text_input(
        "Pantry items (no penalty)",
        value="salt, oil, pepper, water, olive oil"
    )

# --- Trigger / Main logic ---
triggered = st.button("Suggest meals")

if triggered or ingredients_text.strip():
    if not os.path.exists(DATA_PATH):
        st.error(f"Missing recipe file at: {DATA_PATH}. Create data/recipes.json.")
    else:
        try:
            # Parse ingredients
            if use_ai:
                user_ings = parse_ingredients(ingredients_text)
            else:
                user_ings = [x.strip() for x in ingredients_text.split(",") if x.strip()]

            st.caption("Parsed ingredients: " + (", ".join(user_ings) if user_ings else "—"))

            if not user_ings:
                st.info("I couldn't find any ingredients. Try something like: rice, tomato, onion")
            else:
                pantry_items = [x.strip() for x in pantry_text.split(",") if x.strip()]

                # Suggest
                results = suggest_meals(
                    user_ings,
                    top_k=top_k,
                    max_time=max_time,
                    pantry_items=pantry_items
                )

                if not results:
                    st.warning("No matches found with the current filters.")
                else:
                    st.subheader("Top suggestions")
                    all_missing = set()

                    for i, r in enumerate(results, 1):
                        st.markdown(f"### {i}. **{r['title']}**  ({r['time_min']} min)")
                        if r["tags"]:
                            st.caption("Tags: " + ", ".join(r["tags"]))
                        st.markdown(f"✓ **Match:** {', '.join(r['match']) if r['match'] else '—'}")

                        miss_non_pantry = ", ".join(r.get("missing_non_pantry", [])) or "none"
                        st.markdown(f"• **Missing (non-pantry):** {miss_non_pantry}")

                        miss_all = ", ".join(r.get("missing", [])) or "none"
                        st.markdown(f"• **Missing (all):** {miss_all}")

                        all_missing.update(r.get("missing_non_pantry", []))

                        with st.expander("Show steps"):
                            for step in r.get("steps", []):
                                st.write(f"- {step}")

                        st.divider()

                    if all_missing:
                        st.subheader("🛒 Shopping list (non-pantry)")
                        shopping = "\n".join(sorted(all_missing))
                        st.code(shopping)
                        st.download_button("Download shopping list", shopping, file_name="shopping_list.txt")

        except Exception as e:
            st.exception(e)
else:
    st.info("Type your ingredients above and/or click **Suggest meals**.")