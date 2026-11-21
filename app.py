import os
from flask import Flask
from openai import OpenAI

app = Flask(__name__)

client = OpenAI(
    api_key=os.environ.get("GEMINI_API_KEY"),
    base_url="https://generativelanguage.googleapis.com/v1beta/openai/"
)

@app.route("/")
def home():
    reply = client.chat.completions.create(
        model="gemini-3.8-flash",
        messages=[
            {"role": "user", "content": "Tell me a bedtime story about a brave little potato!"}
        ]
    )
    story = reply.choices[0].message.content
    return f"<pre style='white-space: pre-wrap; font-family: sans-serif; padding: 20px;'>{story}</pre>"

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)
