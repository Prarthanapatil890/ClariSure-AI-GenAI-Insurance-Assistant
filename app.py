import streamlit as st
import time
import json
from datetime import datetime, timedelta
from utils.pdf_reader import extract_text_from_pdf
from utils.genai_engine import (
    generate_summary, generate_claim_guidance, generate_letter,
    analyze_premium_breakdown, compare_policies, check_coverage_fit,
    explain_irda_rule, analyze_renewal_change
)
from utils.translator import translate_text
from utils.gemini_engine import query_gemini
from utils.history import load_history, add_to_history, clear_history
from streamlit_chat import message
import plotly.express as px


st.set_page_config(page_title="ClariSure AI", layout="wide", page_icon="📘")


with open("users.json", "r") as f:
    USER_DB = json.load(f)


if "authenticated" not in st.session_state:
    st.session_state.authenticated = False
if "started" not in st.session_state:
    st.session_state.started = False
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []
if "user_id" not in st.session_state:
    st.session_state.user_id = None


if not st.session_state.authenticated:
    st.image("assets/clarisure_logo.png", width=160)
    st.title("🔐 Login to ClariSure AI")
    username = st.text_input("Username")
    password = st.text_input("Password", type="password")
    if st.button("🔓 Login"):
        if username in USER_DB and USER_DB[username] == password:
            st.session_state.authenticated = True
            st.session_state.user_id = username
            st.success("✅ Login successful!")
            time.sleep(1)
            st.experimental_rerun()
        else:
            st.error("❌ Invalid credentials.")
    st.stop()


def show_splash():
    st.markdown("""
        <style>
        .centered {text-align: center;}
        .start-btn {font-size: 20px; width: 200px; margin-top: 20px;}
        </style>
    """, unsafe_allow_html=True)

    st.image("assets/clarisure_logo.png", width=150)
    st.markdown("<h1 class='centered'>🤖 ClariSure AI</h1>", unsafe_allow_html=True)
    st.markdown("<h3 class='centered'>Your GenAI Insurance Assistant</h3>", unsafe_allow_html=True)

    with st.empty():
        for dots in ["", ".", "..", "...", "...."]:
            st.markdown(f"<h5 class='centered'>⏳ Booting ClariSure AI{dots}</h5>", unsafe_allow_html=True)
            time.sleep(0.3)

    st.markdown("<br>", unsafe_allow_html=True)

    if st.button("🚀 Start ClariSure AI", key="start", use_container_width=True):
        st.session_state.started = True
        st.experimental_rerun()


if not st.session_state.started:
    show_splash()
    st.stop()


st.sidebar.image("assets/clarisure_logo.png", width=180)
st.sidebar.markdown("---")
if st.sidebar.button("🚪 Logout"):
    for key in ["authenticated", "started", "chat_history"]:
        st.session_state.pop(key, None)
    st.experimental_rerun()

st.title("📘 ClariSure AI – GenAI Insurance Assistant")
lang = st.sidebar.selectbox("🌐 Choose Output Language", ["English", "Hindi", "Marathi"])


menu = st.sidebar.selectbox("Select Feature", [
    "Policy Explainer", "Premium Breakdown", "Claims Guidance",
    "IRDAI Rule Explainer", "Personalization Check", "Renewal Analyzer",
    "Document Generator", "Policy Comparison", "Notification System", "Insurance Chatbot"
])


with st.sidebar.expander("📜 My History"):
    history = load_history(st.session_state["user_id"])
    if history:
        for entry in reversed(history[-5:]):
            st.markdown(f"**🕒 {entry['time']} – {entry['feature']}**")
            st.markdown(f"🧾 **Input:** {entry['input']}")
            st.markdown(f"💬 **AI:** {entry['response']}")
            st.markdown("---")
    else:
        st.info("No history yet.")
    if st.button("🧹 Clear My History"):
        clear_history(st.session_state["user_id"])
        st.experimental_rerun()


if menu == "Policy Explainer":
    uploaded_file = st.file_uploader("Upload your policy document", type=["pdf"])
    if uploaded_file:
        policy_text = extract_text_from_pdf(uploaded_file)
        if st.button("🧠 Explain Policy"):
            with st.spinner("Generating policy summary..."):
                summary = generate_summary(policy_text)
                translated = translate_text(summary, lang.lower())
            st.markdown(translated if lang != "English" else summary)
            add_to_history(st.session_state["user_id"], menu, "Uploaded Policy", summary)

elif menu == "Premium Breakdown":
    uploaded_file = st.file_uploader("Upload your policy document", type=["pdf"])
    if uploaded_file:
        with st.spinner("Analyzing premium breakdown..."):
            text = extract_text_from_pdf(uploaded_file)
            data = analyze_premium_breakdown(text)

        
        st.subheader("💰 Premium Components Breakdown")
        for component, amount in data.items():
            st.markdown(f"{component}: ₹{amount:,}")

        
        numeric_data = {k: v for k, v in data.items() if isinstance(v, (int, float)) and v > 0}
        if numeric_data:
            fig = px.pie(
                names=numeric_data.keys(),
                values=numeric_data.values(),
                title="📊 Premium Split",
                hole=0.3
            )
            fig.update_traces(textposition='inside', textinfo='percent+label')
            st.plotly_chart(fig)
        else:
            st.warning("No valid numeric data found to display the chart.")
elif menu == "Claims Guidance":
    claim_type = st.selectbox("Select claim type", ["Health", "Motor", "Life", "Travel", "Home"])
    if st.button("📝 Get Claim Checklist"):
        with st.spinner("Fetching checklist..."):
            checklist = generate_claim_guidance(claim_type)
            translated = translate_text(checklist, lang.lower())
        st.markdown(translated if lang != "English" else checklist)
        add_to_history(st.session_state["user_id"], menu, claim_type, checklist)

elif menu == "IRDAI Rule Explainer":
    question = st.text_area("Ask your IRDAI-related question:")
    if st.button("Explain Rule"):
        with st.spinner("Explaining rule..."):
            answer = explain_irda_rule(question)
            translated = translate_text(answer, lang.lower())
        st.markdown(translated if lang != "English" else answer)
        add_to_history(st.session_state["user_id"], menu, question, answer)

elif menu == "Personalization Check":
    age = st.number_input("Age", min_value=18, max_value=100)
    income = st.number_input("Monthly Income (₹)", min_value=0)
    dependents = st.number_input("Dependents", min_value=0)
    if st.button("Check Coverage Fit"):
        with st.spinner("Checking coverage..."):
            result = check_coverage_fit(age, income, dependents)
            translated = translate_text(result, lang.lower())
        st.success(translated if lang != "English" else result)
        add_to_history(st.session_state["user_id"], menu, f"Age: {age}, Income: {income}", result)

elif menu == "Renewal Analyzer":
    old = st.file_uploader("Old Policy", type="pdf")
    new = st.file_uploader("New Policy", type="pdf")
    if old and new and st.button("🔍 Compare"):
        with st.spinner("Analyzing changes..."):
            old_text = extract_text_from_pdf(old)
            new_text = extract_text_from_pdf(new)
            diff = analyze_renewal_change(old_text, new_text)
            translated = translate_text(diff, lang.lower())
        st.code(translated if lang != "English" else diff)
        add_to_history(st.session_state["user_id"], menu, "Old+New PDF", diff)

elif menu == "Document Generator":
    doc_type = st.selectbox("Generate Document For:", ["Nominee Change", "Appeal Rejection"])
    if st.button("📝 Generate Letter"):
        with st.spinner("Generating..."):
            letter = generate_letter("nominee" if "Nominee" in doc_type else "appeal")
            translated = translate_text(letter, lang.lower())
        st.text_area("Generated Letter", translated if lang != "English" else letter, height=250)
        add_to_history(st.session_state["user_id"], menu, doc_type, letter)

elif menu == "Policy Comparison":
    p1 = st.file_uploader("Policy A", type="pdf")
    p2 = st.file_uploader("Policy B", type="pdf")
    if p1 and p2 and st.button("Compare"):
        with st.spinner("Comparing..."):
            t1 = extract_text_from_pdf(p1)
            t2 = extract_text_from_pdf(p2)
            comparison = compare_policies(t1, t2)
            translated = translate_text(comparison, lang.lower())
        st.markdown(translated if lang != "English" else comparison)
        add_to_history(st.session_state["user_id"], menu, "Policy A + B", comparison)

elif menu == "Notification System":
    start = st.date_input("Policy Start Date")
    duration = st.slider("Free-look Period (days)", 5, 30, 15)
    if st.button("Check Deadline"):
        end_date = start + timedelta(days=duration)
        st.info(f"📅 Your Free-look period ends on: **{end_date.strftime('%d %b %Y')}**")

elif menu == "Insurance Chatbot":
    st.subheader("💬 Ask Anything About Insurance")
    user_input = st.chat_input("e.g. What’s the best insurance for a 30-year-old?")
    if user_input:
        with st.spinner("Thinking..."):
            response = query_gemini(user_input)
        st.session_state.chat_history.append({"role": "user", "content": user_input})
        st.session_state.chat_history.append({"role": "bot", "content": response})
        add_to_history(st.session_state["user_id"], menu, user_input, response)

    for i, chat in enumerate(st.session_state.chat_history):
        is_user = chat["role"] == "user"
        message(chat["content"], is_user=is_user, key=str(i))
