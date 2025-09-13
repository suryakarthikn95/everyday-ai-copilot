# 🍳 Everyday AI Copilot — Meal Suggestions

I built this project as part of my portfolio to explore how AI can help with something everyone struggles with: *“What should I cook with what I already have?”*  

The idea is simple:  
- You tell the app what’s in your fridge (either as a short list or a natural sentence like *“I have leftover rice and half an onion”*).  
- It suggests recipes that are quick to make, highlights what you’re missing, and even creates a shopping list for you.  

---

## ✨ What it does
- Understands natural sentences (thanks to OpenAI’s GPT-4o-mini).  
- Filters recipes by cooking time.  
- Lets you define pantry basics (like salt and oil) that don’t count as “missing.”  
- Generates a simple shopping list for non-pantry items.  
- Runs on a clean Streamlit UI you can try locally.  

---

## 🚀 How to run it
Clone the repo and set it up locally:

```bash
git clone https://github.com/suryakarthikn95/everyday-ai-copilot.git
cd everyday-ai-copilot

python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt

# add your OpenAI key in a .env file
echo "OPENAI_API_KEY=sk-..." > .env

python -m streamlit run app.py