import os
from openai import OpenAI
from dotenv import load_dotenv

# Load env vars
load_dotenv()

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

response = client.chat.completions.create(
    model="gpt-3.5-turbo",
    messages=[
        {"role": "system", "content": "You are a friendly assistant."},
        {"role": "user", "content": "Test response please?"}
    ],
    temperature=0.7
)

print(response.choices[0].message.content)
