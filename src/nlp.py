import os, re, json
from typing import List
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()
client = OpenAI()  # uses OPENAI_API_KEY from .env

def _fallback_parse(text: str) -> List[str]:
    """Very simple non-AI fallback so the app still works without API."""
    if not text:
        return []
    parts = re.split(r",| and | & | plus ", text, flags=re.IGNORECASE)
    out = []
    for p in parts:
        p = re.sub(r"[^a-zA-Z\s]", " ", p).strip().lower()
        if p:
            tokens = p.split()
            if tokens:
                out.append(" ".join(tokens[-2:]))  # keep last 1–2 tokens
    # de-dup keep order
    seen, uniq = set(), []
    for i in out:
        if i and i not in seen:
            seen.add(i); uniq.append(i)
    return uniq

def parse_ingredients(text: str) -> List[str]:
    """Use OpenAI to extract a short, normalized ingredient list from free text."""
    if not text:
        return []
    try:
        system = (
            "Extract COOKING INGREDIENTS from the user's sentence. "
            "Return ONLY a JSON array of short, lowercase ingredient names. "
            "No quantities, no brands, no cookware, no adjectives unless essential "
            "(e.g., 'olive oil', 'spring onion')."
        )
        user = f"Text: {text}\nReturn ONLY a JSON array."
        resp = client.chat.completions.create(
            model="gpt-4o-mini",
            temperature=0.0,
            messages=[
                {"role": "system", "content": system},
                {"role": "user", "content": user},
            ],
        )
        raw = resp.choices[0].message.content.strip()
        m = re.search(r"\[.*\]", raw, flags=re.DOTALL)
        if not m:
            return _fallback_parse(text)
        arr = json.loads(m.group(0))
        # normalize + de-dup
        seen, out = set(), []
        for it in arr:
            it = re.sub(r"\s+", " ", str(it).strip().lower())
            if it and it not in seen:
                seen.add(it); out.append(it)
        return out or _fallback_parse(text)
    except Exception:
        return _fallback_parse(text)