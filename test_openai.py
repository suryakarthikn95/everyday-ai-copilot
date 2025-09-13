import os
from dotenv import load_dotenv
from openai import OpenAI

# Load .env file
load_dotenv()
client = OpenAI()

resp = client.chat.completions.create(
    model="gpt-4o-mini",
    messages=[
        {"role": "system", "content": "You are a helpful assistant."},
        {"role": "user", "content": "Say hello, world in one line."}
    ],
)

print("✅ API call succeeded!")
print("Response:", resp.choices[0].message.content)