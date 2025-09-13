from src.nlp import parse_ingredients

samples = [
    "I have leftover rice, half an onion and some spinach.",
    "Only chickpeas, tomato, garlic and a bit of ginger.",
    "Fridge check: tofu + broccoli + bell pepper + soy sauce!!",
]

for s in samples:
    print(s)
    print("->", parse_ingredients(s))
    print()