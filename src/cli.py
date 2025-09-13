import argparse
from src.meal_suggester import suggest_meals

def main():
    parser = argparse.ArgumentParser(description="Meal suggestions from your ingredients.")
    parser.add_argument("--ingredients", "-i", type=str, required=True,
                        help="Comma-separated list, e.g. 'rice, tomato, onion, spinach'")
    parser.add_argument("--topk", "-k", type=int, default=5, help="Number of suggestions")
    args = parser.parse_args()

    user_ings = [x.strip() for x in args.ingredients.split(",")]
    suggestions = suggest_meals(user_ings, top_k=args.topk)

    print("\nYour ingredients:", ", ".join(user_ings))
    print("\nTop suggestions:\n")
    for idx, s in enumerate(suggestions, 1):
        print(f"{idx}. {s['title']}  ({s['time_min']} min)  tags: {', '.join(s['tags'])}")
        print(f"   ✓ match:   {', '.join(s['match']) if s['match'] else '—'}")
        print(f"   • missing: {', '.join(s['missing']) if s['missing'] else 'none'}\n")

if __name__ == "__main__":
    main()