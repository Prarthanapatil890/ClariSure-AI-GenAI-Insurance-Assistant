import os
import google.generativeai as genai

genai.configure(api_key=os.getenv("AIzaSyAmLrLrEsXkKPIhHQH_j42aoKWYV542mbA"))

model = genai.GenerativeModel("models/gemini-1.5-flash")

def translate_text(text, lang="hindi"):
    if lang == "english":
        return text
    prompt = f"Translate this to {lang.capitalize()}:\n\n{text}"
    try:
        response = model.generate_content(prompt)
        return response.text.strip()
    except Exception as e:
        return f"⚠️ Gemini Error: {e}"
