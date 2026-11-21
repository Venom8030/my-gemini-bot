import os
import time
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
    "समुद्र किनारे के एक शांत गाँव का घर",
    "पुराने बरगद के पेड़ के पास बना अकेला बंगला",
    "कोहरे से ढकी एक पुरानी चाय बागान की कोठी"
]

OBJECTS = [
    "एक अतिरिक्त पीतल का लोटा",
    "छत पर रखी एक बंद संदूक",
    "रात 1:15 बजे बजने वाली पुरानी घड़ी",
    "आँगन के नीम के पेड़ पर बँधा लाल धागा",
    "रसोई में रोज़ रात रखा जाने वाला दूध का कटोरा",
    "सीढ़ियों के नीचे वाला बंद कमरा",
    "पुराना रेडियो जो बिना सेल के चलता है",
    "घर के मुख्य दरवाज़े पर लटका पुराना ताला",
    "बरामदे में उल्टा रखा हुआ मिट्टी का घड़ा",
    "रात 12 बजे के बाद बजने वाली पीतल की घंटी"
]

SYSTEM_PROMPT = """
You are a master Hindi horror & mystery YouTube scriptwriter. Write 100% original, copyright-free, deeply atmospheric Hindi stories designed for long-form YouTube narration (around 950 to 1,150 words).

Follow this exact storytelling structure and style:
1. THE "ODD RULE" HOOK: Start in first-person ("मैं...") with a strange daily family rule or mysterious habit that breaks normal logic, plus a strict warning from an elder (Dadi, Baba, Kaka, or Ma).
2. RISING TENSION & SENSORY DETAILS: Use crisp, gripping Hindi sentences (Devanagari script only). Include exact night timestamps (like रात 2:15 बजे), temperature changes (बर्फ जैसा ठंडा), strange sounds (खट-खट, फुसफुसाहट), and psychological dread.
3. BREAKING THE RULE: Show why and how the protagonist accidentally breaks the rule, leading to an eerie encounter (such as voice mimicry, shadows, or an uninvited presence).
4. UNCANNY TWIST & CHILLING ENDING: End with a haunting new rule the family must now follow, and a final spine-chilling twist in the last two lines.
5. SCENE-BY-SCENE FORMAT: Break the entire story into 12 to 14 numbered scenes (Scene 1 to Scene 14). For each scene, provide:
   - [Visual Prompt / दृश्य]: A clear, dark, cinematic visual description for AI image/video generation.
   - [SFX / आवाज़]: Specific background sound effects for editing (e.g., slow footsteps, creaking wooden door, wind howling, clock ticking).
   - [Narration / वॉइसओवर]: The exact Hindi voiceover script for that scene (3 to 5 gripping sentences per scene).

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
        timeout=35.0
    )

    chosen_setting = random.choice(SETTINGS)
    chosen_object = random.choice(OBJECTS)
    user_prompt = (
        f"Write a brand-new, long Hindi horror/mystery YouTube story set in: {chosen_setting}. "
        f"Center the strange family rule around: {chosen_object}. "
        f"Break it down into 12 to 14 detailed scenes with Visual Prompt, SFX, and Hindi Narration."
    )

    last_error = ""
    for model_name in ["gemini-3.8-flash", "gemini-3.5-flash-lite"]:
        try:
            reply = client.chat.completions.create(
                model=model_name,
                temperature=0.95,
                max_tokens=3000,
                messages=[
                    {"role": "system", "content": SYSTEM_PROMPT},
                    {"role": "user", "content": user_prompt}
                ]
            )
            return reply.choices[0].message.content
        except Exception as e:
            last_error = f"{model_name}: {str(e)}"
            time.sleep(2)

    return f"Free quota temporarily busy. Wait 30 seconds and click Generate again.\n\nDetails:\n{last_error}"

@app.route("/")
def home():
    try:
        story_html = ""
        copy_btn = ""
        if request.args.get("generate") == "1":
            story = generate_story()
            copy_btn = (
                "<button id='copyBtn' onclick='copyStory()' "
                "style='margin-left: 12px; padding: 12px 22px; background: #2e7d32; color: white; "
                "border: none; border-radius: 8px; font-weight: bold; font-size: 16px; cursor: pointer;'>"
                "Copy Script</button>"
            )
            story_html = (
                f"<pre id='storyBox' style='white-space: pre-wrap; font-family: inherit; "
                f"margin-top: 24px; background: #1a1a1a; padding: 20px; border-radius: 8px;'>{story}</pre>"
            )

        return (
            "<div style='max-width: 860px; margin: 40px auto; padding: 24px; "
            "background: #121212; color: #f1f1f1; border-radius: 12px; "
            "font-family: sans-serif; line-height: 1.8; font-size: 18px;'>"
            "<h2 style='margin-top: 0;'>Hindi Horror Story Generator</h2>"
            "<a href='/?generate=1' onclick=\"this.innerText='Writing 12-14 scenes (~15 sec)...'\" "
            "style='display: inline-block; padding: 12px 22px; background: #e53935; color: white; "
            "text-decoration: none; border-radius: 8px; font-weight: bold; font-size: 16px;'>"
            "Generate New Hindi Story</a>"
            f"{copy_btn}"
            f"{story_html}"
            "<script>"
            "function copyStory() {"
            "  var text = document.getElementById('storyBox').innerText;"
            "  navigator.clipboard.writeText(text).then(function() {"
            "    var btn = document.getElementById('copyBtn');"
            "    btn.innerText = 'Copied!';"
            "    setTimeout(function(){ btn.innerText = 'Copy Script'; }, 2000);"
            "  });"
            "}"
            "</script>"
            "</div>"
        )
    except Exception:
        return f"<pre>{traceback.format_exc()}</pre>"

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)
