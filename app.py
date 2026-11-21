import os
from openai import OpenAI

# Connect your walkie-talkie to Google's free Gemini brain
client = OpenAI(
    api_key=os.environ.get("GEMINI_API_KEY"),
    base_url="https://generativelanguage.googleapis.com/v1beta/openai/"
)

# Ask Gemini a question!
reply = client.chat.completions.create(
    model="gemini-3.8-flash",
    messages=[
        {"role": "user", "content": "Tell me a bedtime story about a brave little potato!"}
    ]
)

print(reply.choices[0].message.content)
