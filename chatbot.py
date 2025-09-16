import streamlit as st
import google.generativeai as genai
import datetime
import pandas as pd
from deep_translator import GoogleTranslator

# --------------------------
# CONFIGURE GEMINI
# --------------------------
genai.configure(api_key="YOUR_API_KEY_HERE")  # ⚠️ Replace before running
model = genai.GenerativeModel("gemini-1.5-flash")

# --------------------------
# PAGE SETTINGS
# --------------------------
st.set_page_config(page_title="Youth Mental Wellness Chatbot", page_icon="💙", layout="wide")

# --------------------------
# CUSTOM CSS (UI/UX)
# --------------------------
st.markdown("""
    <style>
        .main {
            background: #f9faff;
        }
        .stApp {
            background: linear-gradient(135deg, #e0f7fa, #fce4ec);
        }
        .header {
            text-align: center;
            font-size: 32px;
            font-weight: bold;
            padding: 15px;
            color: white;
            border-radius: 10px;
            background: linear-gradient(90deg, #6a11cb 0%, #2575fc 100%);
            margin-bottom: 20px;
        }
        .chat-container {
            padding: 15px;
            background: white;
            border-radius: 10px;
            box-shadow: 0px 2px 6px rgba(0,0,0,0.1);
        }
        .user-msg {
            background: #cce5ff;
            padding: 8px 12px;
            border-radius: 10px;
            margin: 5px 0;
        }
        .bot-msg {
            background: #d4edda;
            padding: 8px 12px;
            border-radius: 10px;
            margin: 5px 0;
        }
    </style>
""", unsafe_allow_html=True)

# --------------------------
# HEADER
# --------------------------
st.markdown('<div class="header">💙 Youth Mental Wellness Chatbot 💙</div>', unsafe_allow_html=True)
st.write("Confidential, empathetic AI support for students — anytime, anywhere.")

# --------------------------
# SIDEBAR
# --------------------------
st.sidebar.title("⚙️ Settings")
language = st.sidebar.selectbox("🌍 Choose your language", ["English", "Hindi", "Kannada"])
st.sidebar.markdown("### 💡 Tips")
st.sidebar.write("👉 Type your feelings below\n👉 Log moods daily\n👉 Use 🚨 Panic Button if needed")

# --------------------------
# CHAT HISTORY
# --------------------------
st.markdown("### 💬 Chat")
if "messages" not in st.session_state:
    st.session_state["messages"] = []

with st.container():
    for msg in st.session_state["messages"]:
        if msg["role"] == "user":
            st.markdown(f"<div class='user-msg'><b>You:</b> {msg['content']}</div>", unsafe_allow_html=True)
        else:
            st.markdown(f"<div class='bot-msg'><b>Bot:</b> {msg['content']}</div>", unsafe_allow_html=True)

# --------------------------
# CHAT INPUT
# --------------------------
if prompt := st.chat_input("How are you feeling today?"):
    # Translate user input
    if language != "English":
        prompt_translated = GoogleTranslator(source="auto", target="en").translate(prompt)
    else:
        prompt_translated = prompt

    # Save user input
    st.session_state["messages"].append({"role": "user", "content": prompt})

    try:
        # Generate AI reply
        response = model.generate_content(
            f"You are a supportive, empathetic mental wellness assistant for young students. "
            f"Always be encouraging, confidential, and positive. Avoid medical advice. "
            f"User said: {prompt_translated}"
        )
        reply = response.text

        # Translate reply if needed
        if language != "English":
            reply = GoogleTranslator(source="en", target=language.lower()).translate(reply)

    except Exception as e:
        reply = f"⚠️ Error: {str(e)}"

    st.session_state["messages"].append({"role": "assistant", "content": reply})

# --------------------------
# PANIC BUTTON
# --------------------------
st.markdown("---")
if st.button("🚨 Panic Button – Get Help", use_container_width=True):
    st.error("💡 If you’re feeling overwhelmed, please reach out to someone you trust or call a helpline.")
    st.info("📞 India Helpline: 9152987821 (KIRAN - National Mental Health Helpline)\n\n📞 Emergency: 112")

# --------------------------
# MOOD TRACKER
# --------------------------
st.markdown("### 📊 Mood Tracker")
if "mood_log" not in st.session_state:
    st.session_state["mood_log"] = []

mood = st.selectbox("How do you feel today?", ["😊 Happy", "😟 Stressed", "😐 Neutral", "😭 Sad"])
if st.button("Log Mood"):
    st.session_state["mood_log"].append({"date": datetime.date.today(), "mood": mood})
    st.success("✅ Mood logged successfully!")

# Show mood chart
if st.session_state["mood_log"]:
    df = pd.DataFrame(st.session_state["mood_log"])
    mood_map = {"😊 Happy": 3, "😟 Stressed": 1, "😐 Neutral": 2, "😭 Sad": 0}
    df["mood_score"] = df["mood"].map(mood_map)
    st.line_chart(df.set_index("date")["mood_score"])
