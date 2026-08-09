import streamlit as st

# Page Configuration
st.set_page_config(page_title="Boss's AI Boardroom", page_icon="🧠", layout="centered")

# Custom CSS for Dark Theme, WhatsApp Style & Animations
st.markdown("""
    <style>
    .stApp {
        background-color: #0e1117;
        color: #ffffff;
    }
    .chat-bubble-boss {
        background-color: #005c4b;
        padding: 10px 15px;
        border-radius: 15px 15px 0px 15px;
        margin: 5px 0;
        float: right;
        max-width: 70%;
    }
    .chat-bubble-ai {
        background-color: #202c33;
        padding: 10px 15px;
        border-radius: 15px 15px 15px 0px;
        margin: 5px 0;
        float: left;
        max-width: 70%;
        border-left: 4px solid #00a884;
    }
    .boss-title {
        text-align: center;
        color: #00a884;
        font-weight: bold;
        text-shadow: 0px 0px 10px rgba(0, 168, 132, 0.5);
    }
    </style>
""", unsafe_allow_html=True)

# App Header
st.markdown("<h1 class='boss-title'>🧠 Boss's AI Boardroom</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center; color: #8696a0;'>Advanced AI Multi-Agent Group | Status: Online 🟢</p>", unsafe_allow_html=True)
st.markdown("---")

# Chat History Simulation
if "messages" not in st.session_state:
    st.session_state.messages = [
        {"role": "ai", "content": "Hello Boss! Senior Developer and Code Reviewer are ready. What is your command today?"}
    ]

# Display Chat Messages
for msg in st.session_state.messages:
    if msg["role"] == "boss":
        st.markdown(f"<div class='chat-bubble-boss'><b>You (Boss):</b><br>{msg['content']}</div>", unsafe_allow_html=True)
    else:
        st.markdown(f"<div class='chat-bubble-ai'><b>AI Team:</b><br>{msg['content']}</div>", unsafe_allow_html=True)

# User Input Box (WhatsApp Style)
st.markdown("<br><br>", unsafe_allow_html=True)
user_input = st.text_input("Type your command for the AI team, Boss...")

col1, col2, col3 = st.columns([1, 1, 4])
with col1:
    send_btn = st.button("Send 🚀")
with col2:
    clear_btn = st.button("Clear Chat 🔄")

if send_btn and user_input:
    st.session_state.messages.append({"role": "boss", "content": user_input})
    # Simulated multi-agent response response
    ai_reply = f"Boss, analyzing your request: '{user_input}'. Senior Developer and Code Reviewer are cross-checking the solution for you right now!"
    st.session_state.messages.append({"role": "ai", "content": ai_reply})
    st.rerun()

if clear_btn:
    st.session_state.messages = []
    st.rerun()
  
