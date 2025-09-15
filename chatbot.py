import streamlit as st
import google.generativeai as genai
import datetime
import pandas as pd
from deep_translator import GoogleTranslator

# Configure Gemini with your API key (⚠️ replace with your real key before running locally)
genai.configure(api_key="YOUR_API_KEY_HERE")

# Load model
model = genai.GenerativeModel("gemini-1.5-flash")

# Streamlit UI Setup
st.set_page_config(page_title="Youth Mental Wellness Chatbot", page_icon="💬", layout="centered")

# Sidebar for language selection
st.sidebar.title("🌐 Settings")
language = st.sidebar.selectbox("Choose your language", ["English", "Hindi", "Kannada"])

# App title
st.title("💬 Confidential Youth Mental Wellness Chatbot")
st.write("This AI-powered chatbot provides a safe, supportive space for youth to talk about their feelings.")

# Panic button
if st.button("🚨 Panic Button – Get Help"):
    st.warning("If you’re feeling overwhelmed, please reach out to a trusted person or call a helpline.")
    st.write("📞 India Helpline: 9152987821 (KIRAN - National Mental Health Helpline)")
    st.write("📞 Emergency: 112")

st.markdown("---")

# Chat history
if "messages" not in st.session_state:
    st.session_state["messages"] = []

# Display past messages
for msg in st.session_state["messages"]:
    st.chat_message(msg["role"]).write(msg["content"])

# User input
if prompt := st.chat_input("How are you feeling today?"):
    # Translate if not English
    if language != "English":
        prompt_translated = GoogleTranslator(source="auto", target="en").translate(prompt)
    else:
        prompt_translated = prompt

    # Add user message
    st.session_state["messages"].append({"role": "user", "content": prompt})
    st.chat_message("user").write(prompt)

    # AI response with supportive context
    response = model.generate_content(
        f"You are a supportive, empathetic mental wellness assistant for young students. "
        f"Always be encouraging, confidential, and positive. Avoid medical advice. "
        f"User said: {prompt_translated}"
    )
    reply = response.text

    # Translate back if needed
    if language != "English":
        reply = GoogleTranslator(source="en", target=language.lower()).translate(reply)

    # Add AI reply
    st.session_state["messages"].append({"role": "assistant", "content": reply})
    st.chat_message("assistant").write(reply)

# Mood Tracker
st.markdown("---")
st.subheader("📊 Mood Tracker")

if "mood_log" not in st.session_state:
    st.session_state["mood_log"] = []

mood = st.selectbox("How do you feel today?", ["😊 Happy", "😟 Stressed", "😐 Neutral", "😭 Sad"])

if st.button("Log Mood"):
    st.session_state["mood_log"].append({"date": datetime.date.today(), "mood": mood})
    st.success("✅ Mood logged successfully!")

# Show mood history chart
if st.session_state["mood_log"]:
    df = pd.DataFrame(st.session_state["mood_log"])
    mood_map = {"😊 Happy": 3, "😟 Stressed": 1, "😐 Neutral": 2, "😭 Sad": 0}
    df["mood_score"] = df["mood"].map(mood_map)
    st.line_chart(df.set_index("date")["mood_score"])
