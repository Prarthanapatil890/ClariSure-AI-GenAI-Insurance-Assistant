

import os
import google.generativeai as genai
from dotenv import load_dotenv
load_dotenv()

genai.configure(api_key=os.getenv("AIzaSyAmLrLrEsXkKPIhHQH_j42aoKWYV542mbA"))

def query_gemini(prompt):
    try:
        model = genai.GenerativeModel("models/gemini-1.5-flash")
        response = model.generate_content(prompt)
        return response.text.strip()
    except Exception as e:
        return f"⚠️ Gemini API Error: {e}"
