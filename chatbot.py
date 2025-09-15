import streamlit as st
import google.generativeai as genai
import datetime
import pandas as pd
from deep_translator import GoogleTranslator

# --------------------------
# CONFIGURE GEMINI (from Streamlit Secrets)
# --------------------------
api_key = st.secrets["GEMINI_API_KEY"]  # ✅ Correct: must match secrets.toml
genai.configure(api_key=api_key)

try:
    model = genai.GenerativeModel("models/gemini-1.5-flash")  # ✅ FIXED
except Exception as e:
    st.error(f"⚠️ Gemini init failed: {str(e)}")
    st.stop()


# --------------------------
# PAGE SETTINGS
# --------------------------
st.set_page_config(page_title="Youth Mental Wellness Chatbot", page_icon="💙", layout="wide")

# Custom CSS
st.markdown("""
    <style>
        .main {
            background: linear-gradient(135deg, #f3e7ff 0%, #e3f6f5 100%);
        }
        .user-msg {
            background-color: #cce5ff;
            padding: 10px;
            border-radius: 10px;
            margin: 5px 0;
        }
        .bot-msg {
            background-color: #d4edda;
            padding: 10px;
            border-radius: 10px;
            margin: 5px 0;
        }
        .header {
            font-size: 28px;
            padding: 15px;
            border-radius: 8px;
            text-align: center;
            background: linear-gradient(90deg, #6a11cb 0%, #2575fc 100%);
            color: white;
        }
    </style>
""", unsafe_allow_html=True)

# --------------------------
# HEADER
# --------------------------
st.markdown('<div class="header">🌟 Youth Mental Wellness Chatbot 🌟</div>', unsafe_allow_html=True)
st.write("💙 Confidential, empathetic AI support for students — anytime, anywhere.")

# --------------------------
# SIDEBAR
# --------------------------
st.sidebar.title("⚙️ Settings")
lang = st.sidebar.selectbox("🌍 Language", ["en", "hi", "kn"], index=0)
st.sidebar.markdown("---")
st.sidebar.write("💡 **Tips:**\n- Type your feelings below\n- Log moods daily\n- Use 🚨 Panic Button if needed")

# --------------------------
# SESSION STATE
# --------------------------
if "messages" not in st.session_state:
    st.session_state["messages"] = []
if "mood_log" not in st.session_state:
    st.session_state["mood_log"] = []

# --------------------------
# CHAT DISPLAY
# --------------------------
st.subheader("💬 Chat")
for msg in st.session_state["messages"]:
    css_class = "user-msg" if msg["role"] == "user" else "bot-msg"
    st.markdown(f"<div class='{css_class}'><b>{msg['role'].capitalize()}:</b> {msg['content']}</div>", unsafe_allow_html=True)

# --------------------------
# CHAT INPUT
# --------------------------
if prompt := st.chat_input("How are you feeling today?"):
    translated_prompt = GoogleTranslator(source="auto", target="en").translate(prompt)
    st.session_state["messages"].append({"role": "user", "content": prompt})

    try:
        # Sentiment detection
        sentiment_resp = model.generate_content(
            f"Classify this text as Positive, Neutral, or Negative: {translated_prompt}"
        )
        sentiment_check = sentiment_resp.text.strip() if hasattr(sentiment_resp, "text") else "Neutral"

        # AI response
        response = model.generate_content(
            f"You are a kind, empathetic assistant. "
            f"User sentiment: {sentiment_check}. "
            f"Respond with encouragement and positivity. "
            f"User said: {translated_prompt}"
        )
        reply_text = response.text if hasattr(response, "text") else "I'm here to support you 💙"
        reply = GoogleTranslator(source="en", target=lang).translate(reply_text)

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
st.subheader("📊 Mood Tracker")
mood = st.selectbox("How do you feel today?", ["😊 Happy", "😟 Stressed", "😐 Neutral", "😭 Sad"])

if st.button("Log Mood"):
    st.session_state["mood_log"].append({"date": datetime.date.today(), "mood": mood})
    st.success("✔ Mood logged successfully!")

if st.session_state["mood_log"]:
    df = pd.DataFrame(st.session_state["mood_log"])
    mood_map = {"😊 Happy": 0, "😟 Stressed": 1, "😐 Neutral": 2, "😭 Sad": 3}
    df["mood_index"] = df["mood"].map(mood_map)
    st.line_chart(df.set_index("date")["mood_index"])
    st.caption("Y-axis: 0=Happy, 1=Stressed, 2=Neutral, 3=Sad")

# --------------------------
# JOURNAL DOWNLOAD
# --------------------------
if st.button("📥 Download My Journal", use_container_width=True):
    log = "=== Chat History ===\n"
    for msg in st.session_state["messages"]:
        log += f"{msg['role'].capitalize()}: {msg['content']}\n"
    log += "\n=== Mood Log ===\n"
    for entry in st.session_state["mood_log"]:
        log += f"{entry['date']} - {entry['mood']}\n"
    st.download_button("⬇ Save Journal", log, file_name="my_wellness_journal.txt")
