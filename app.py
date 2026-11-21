import os
import random
import traceback
from flask import Flask, request
from openai import OpenAI

app = Flask(__name__)

SETTINGS = [
    "एक पुराने पहाड़ी गाँव का लकड़ी का घर",
    "राजस्थान की एक सुनसान हवेली के पास का कुआँ",
    "कोंकण के घने जंगल के किनारे बना पुश्तैनी घर",
    "बनारस की एक संकरी गली का पुराना मकान",
    "रेलवे क्रॉसिंग के पास बना सुनसान क्वार्टर",
    "नदी किनारे बने पुराने मंदिर के पीछे का घर",
    "एक पुराने आम के बगीचे के बीच बना फार्महाउस",
    "समुद्र किनारे के एक शांत गाँव का घर"
]

OBJECTS = [
    "एक अतिरिक्त पीतल का लोटा",
    "छत पर रखी एक बंद संदूक",
    "रात 1:15 बजे बजने वाली पुरानी घड़ी",
    "आँगन के नीम के पेड़ पर बँधा लाल धागा",
    "रसोई में रोज़ रात रखा जाने वाला दूध का कटोरा",
    "सीढ़ियों के नीचे वाला बंद कमरा",
    "पुराना रेडियो जो बिना सेल के चलता है",
    "घर के मुख्य दरवाज़े पर लटका पुराना ताला"
]

SYSTEM_PROMPT = """
You are a master Hindi horror & mystery YouTube scriptwriter. Write 100% original, copyright-free, atmospheric Hindi stories designed for YouTube narration (around 650 to 800 words).

Follow this exact storytelling structure and style:
1. THE "ODD RULE" HOOK: Start in first-person ("मैं...") with a strange daily family rule or mysterious habit that breaks normal logic, plus a strict warning from an elder (Dadi, Baba, Kaka, or Ma).
2. RISING TENSION & SENSORY DETAILS: Use crisp, gripping Hindi sentences (Devanagari script only). Include exact night timestamps (like रात 2:15 बजे), temperature changes (बर्फ जैसा ठंडा), strange sounds (खट-खट, फुसफुसाहट), and psychological dread.
3. BREAKING THE RULE: Show why and how the protagonist accidentally breaks the rule, leading to an eerie encounter (such as mimicry, shadows, or an uninvited presence).
4. UNCANNY TWIST & CHILLING ENDING: End with a haunting new rule the family must now follow, and a final spine-chilling twist in the last two lines.
5. SCENE-BY-SCENE FORMAT: Break the entire story into 10 numbered scenes (Scene 1 to Scene 10). For each scene, provide:
   - [Visual Prompt / दृश्य]: A concise 1-sentence description of the dark, moody scene for video generation.
   - [Narration / वॉइसओवर]: The exact Hindi voiceover script for that scene.

Rules:
- Invent completely fresh Indian character names, relationships, and backstories every single time.
- Never repeat the "Paanchvi Roti" (five rotis) plot.
- Start with a catchy Hindi YouTube Title at the very top.
"""

def generate_story():
    api_key = os.environ.get("GEMINI_API_KEY", "").strip()
    if not api_key:
        return "ERROR: GEMINI_API_KEY is missing in Render Environment Variables!"

    client = OpenAI(
        api_key=api_key,
        base_url="https://generativelanguage.googleapis.com/v1beta/openai/",
        timeout=25.0
    )

    chosen_setting = random.choice(SETTINGS)
    chosen_object = random.choice(OBJECTS)
    user_prompt = (
        f"Write a brand-new Hindi horror/mystery YouTube story set in: {chosen_setting}. "
        f"Center the strange family rule around: {chosen_object}. "
        f"Break it down into 10 numbered scenes."
    )

    try:
        reply = client.chat.completions.create(
            model="gemini-3.8-flash",
            temperature=0.95,
            max_tokens=1800,
            messages=[
                {"role": "system", "content": SYSTEM_PROMPT},
                {"role": "user", "content": user_prompt}
            ]
        )
        return reply.choices[0].message.content
    except Exception as e:
        return f"Error from Gemini API:\n{str(e)}"

@app.route("/")
def home():
    try:
        story_html = ""
        if request.args.get("generate") == "1":
            story = generate_story()
            story_html = f"<pre style='white-space: pre-wrap; font-family: inherit; margin-top: 24px;'>{story}</pre>"

        return (
            "<div style='max-width: 820px; margin: 40px auto; padding: 24px; "
            "background: #121212; color: #f1f1f1; border-radius: 12px; "
            "font-family: sans-serif; line-height: 1.8; font-size: 18px;'>"
            "<h2 style='margin-top: 0;'>Hindi Horror Story Generator</h2>"
            "<a href='/?generate=1' onclick=\"this.innerText='Writing your story (~10 sec)...'\" "
            "style='display: inline-block; padding: 12px 22px; background: #e53935; color: white; "
            "text-decoration: none; border-radius: 8px; font-weight: bold;'>"
            "Generate New Hindi Story</a>"
            f"{story_html}"
            "</div>"
        )
    except Exception:
        return f"<pre>{traceback.format_exc()}</pre>"

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)
