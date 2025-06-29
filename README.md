
# 🤖 ClariSure AI – GenAI-Powered Insurance Assistant

ClariSure AI is a Generative AI agent designed to simplify and personalize the insurance experience for users. It explains complex policy terms, compares documents, generates letters, and provides IRDAI regulation answers – all in a conversational UI with multilingual support and personalized history tracking.


## 🚀 Features

| Category                | Feature                             | Description                                                       |
|-------------------------|-------------------------------------|-------------------------------------------------------------------|
| 🗣️ User Interaction     | Chatbot Interface                   | Ask general insurance questions in natural language               |
| 📄 Policy Understanding | Policy Explainer                    | Upload and summarize policy PDFs                                  |
| 💰 Transparency         | Premium Breakdown                   | Break down premium into Risk Cover, Admin, GST                    |
| 📝 Claims Assistance    | Claims Checklist                    | Shows documents and steps for Health, Life, Motor, etc.           |
| ⚖️ IRDAI Rule Clarity   | IRDAI Rule Explainer                | Ask any question based on IRDAI regulations                       |
| 🧍 Personalization      | Coverage Fit Checker                | Suggests coverage based on user’s profile                         |
| 🔄 Renewals             | Renewal Analyzer                    | Highlights differences between old and new policy PDFs            |
| 🏷️ Document Help        | Letter Generator                    | Nominee update or claim appeal letter                             |
| 📊 Policy Comparison    | Compare Policies                    | Compares two uploaded insurance documents                         |
| 🌐 Multilingual         | Hindi/Marathi Support               | Translate any response into Hindi or Marathi                      |
| 🧠 Chatbot              | Gemini-powered Insurance Q&A        | Ask anything – best plan, LIC terms, fraud spotting               |
| 🧾 History              | Per-user History + Clear Option     | Track past inputs and responses in sidebar                        |
| 🛡️ Login                | Secure Session per User             | Fixed users with username/password                                |

---

## 🛠️ Tech Stack

- **Frontend**: Streamlit + CSS + Streamlit Chat
- **Backend**: Python
- **LLM (Local)**: Ollama running `gemma:2b` for core features
- **LLM (API)**: Google Gemini API (for multilingual translation and chatbot)
- **Others**: Plotly, PyMuPDF, JSON, OS

---

## 📂 Project Structure

clarisure-ai/
│
├── app.py # Main Streamlit UI with all features
├── users.json # Stores fixed login credentials
├── history_data/ # Per-user history .json files
│
├── utils/
│ ├── genai_engine.py # Uses Ollama (Gemma 2B) for all feature prompts
│ ├── gemini_engine.py # Gemini API: Insurance chatbot
│ ├── translator.py # Gemini-powered multilingual translation
│ ├── pdf_reader.py # Extracts text from uploaded PDFs
│ └── history.py # Load, write, clear per-user history
│
├── assets/
│ └── clarisure_logo.png # App logo for sidebar and splash
│
├── .streamlit/
│ └── config.toml # Optional Streamlit theming
│
├── requirements.txt # Python dependencies
└── README.md # You are here!

## 🧪 Setup Instructions

✅ 1. Clone the Repository

git clone 
cd clarisure-ai

✅ 2. Install Dependencies

Make sure Python 3.10+ is installed.
pip install -r requirements.txt

✅ 3. Run Ollama Locally with Gemma

Install Ollama if not installed: https://ollama.com/download
ollama run gemma:2b

✅ 4. Set Gemini API Key

Create a .env file (or use your terminal) and set:
GOOGLE_API_KEY=your-gemini-api-key
Make sure the Gemini key has access to gemini-1.5-flash

✅ 5. Launch the App

streamlit run app.py

🔐 Login Credentials (users.json)

{
  "admin": "prarthana",
  "user1": "mypassword"
}


📌 Demo Ideas

Upload a health policy PDF → get summary
Try Premium Breakdown → Pie Chart
Ask IRDAI question: "What is the maximum time allowed to settle a claim?"
Use the chatbot → Ask: "Best policy for 35-year-old with ₹10L salary"
Translate to Hindi/Marathi using the dropdown

🧭 Future Scope

Integrate real-time fraud alerts from APIs
Add voice input/output
Allow Excel/CSV policy import
Integrate policy recommendations based on real-time premium comparison
