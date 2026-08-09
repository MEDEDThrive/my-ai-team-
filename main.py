import streamlit as st
import google.generativeai as genai
import time

# Page Configuration
st.set_page_config(
    page_title="My AI Team - Ultra Command Center",
    page_icon="⚡",
    layout="centered"
)

# Custom Cyberpunk & WhatsApp Dark Theme CSS with Glassmorphism
st.markdown("""
    <style>
    .stApp {
        background-color: #0b141a;
        color: #e9edef;
    }
    .splash-container {
        text-align: center;
        padding: 50px 20px;
        background: linear-gradient(135deg, #111b21 0%, #0b141a 100%);
        border: 1px solid #00ff88;
        border-radius: 15px;
        box-shadow: 0 0 20px rgba(0, 255, 136, 0.2);
        margin-top: 50px;
    }
    .chat-bubble-user {
        background-color: #005c4b;
        color: #e9edef;
        padding: 14px 18px;
        border-radius: 12px 0px 12px 12px;
        margin: 10px 0;
        max-width: 85%;
        float: right;
        clear: both;
        box-shadow: 0 0 10px rgba(0, 255, 128, 0.2);
    }
    .chat-bubble-agent {
        background-color: #202c33;
        color: #e9edef;
        padding: 14px 18px;
        border-radius: 0px 12px 12px 12px;
        margin: 10px 0;
        max-width: 85%;
        float: left;
        clear: both;
        border-left: 4px solid #00ff88;
        box-shadow: 0 0 15px rgba(0, 255, 136, 0.15);
    }
    .agent-title {
        font-size: 12px;
        color: #00ff88;
        font-weight: bold;
        margin-bottom: 6px;
        text-transform: uppercase;
        letter-spacing: 1px;
    }
    .stTextInput input {
        background-color: #202c33 !important;
        color: #e9edef !important;
        border: 1px solid #2a3942 !important;
        border-radius: 8px !important;
    }
    </style>
""", unsafe_allow_html=True)

# Session State Initializations
if "initialized" not in st.session_state:
    st.session_state.initialized = False
if "messages" not in st.session_state:
    st.session_state.messages = []
if "is_locked" not in st.session_state:
    st.session_state.is_locked = False

# 1. Starting Splash Animation Screen
if not st.session_state.initialized:
    placeholder = st.empty()
    with placeholder.container():
        st.markdown("""
            <div class="splash-container">
                <h1 style="color: #00ff88; font-family: monospace;">⚡ NEURAL CORE INITIALIZING ⚡</h1>
                <p style="color: #8696a0; font-size: 16px;">Loading 10 Elite AI Agents into the grid...</p>
            </div>
        """, unsafe_allow_html=True)
        
        progress_bar = st.progress(0)
        for i in range(100):
            time.sleep(0.01)
            progress_bar.progress(i + 1)
        time.sleep(0.5)
    placeholder.empty()
    st.session_state.initialized = True
    st.rerun()

# Sidebar Navigation & Controls
with st.sidebar:
    st.markdown("### ⚡ COMMAND CONTROLS")
    api_key = st.text_input("Enter Gemini API Key", type="password")
    
    st.markdown("---")
    st.markdown("### 🔐 Security Panel")
    lock_toggle = st.checkbox("Lock Chat (Boss Privacy)", value=st.session_state.is_locked)
    if lock_toggle != st.session_state.is_locked:
        st.session_state.is_locked = lock_toggle
        st.rerun()

    st.markdown("---")
    st.markdown("### 🤖 The 10-Agent Squad")
    agents_list = [
        "1. Senior Architect", "2. Code Reviewer", "3. Cyber-Security", 
        "4. UI/UX Stylist", "5. Database Expert", "6. Troubleshooter", 
        "7. Performance Optimizer", "8. Technical Writer", "9. QA Tester", "10. Project Manager (Lead)"
    ]
    for agent in agents_list:
        st.markdown(f"🟢 {agent}")

# Main Header
st.markdown("### ⚡ MULTI-AGENT COMMAND CENTER")
st.markdown("<p style='color: #8696a0; font-size: 14px;'>Welcome back, Boss. Your elite autonomous squad is locked and loaded.</p>", unsafe_allow_html=True)
st.markdown("---")

# Chat Lock Verification
if st.session_state.is_locked:
    st.warning("🔒 **System Locked by Boss Security.** Please disable the lock in the sidebar to view the command grid.")
else:
    # Display Chat History
    for message in st.session_state.messages:
        if message["role"] == "user":
            st.markdown(f'<div class="chat-bubble-user"><b>Boss:</b><br>{message["content"]}</div>', unsafe_allow_html=True)
        else:
            st.markdown(f'''
                <div class="chat-bubble-agent">
                    <div class="agent-title">{message["agent"]}</div>
                    {message["content"]}
                </div>
            ''', unsafe_allow_html=True)

    # User Command Input
    user_prompt = st.chat_input("Issue your command, Boss...")

    if user_prompt:
        if not api_key:
            st.warning("⚠️ Please provide your Gemini API Key in the sidebar first, Boss!")
        else:
            st.session_state.messages.append({"role": "user", "content": user_prompt})
            
            genai.configure(api_key=api_key)
            model = genai.GenerativeModel('gemini-1.5-flash')

            # Multi-Agent Workflow Simulation
            with st.spinner("Senior Architect is designing the core blueprint..."):
                arch_prompt = f"You are the Senior Architect agent. Formulate a technical blueprint for Boss based on: {user_prompt}"
                arch_res = model.generate_content(arch_prompt).text

            with st.spinner("Code Reviewer & Cyber-Security are auditing the solution..."):
                audit_prompt = f"You are the Code Reviewer and Security Expert. Audit and optimize this architecture for Boss: \n{arch_res}"
                audit_res = model.generate_content(audit_prompt).text

            with st.spinner("Project Manager is orchestrating the final output for Boss..."):
                pm_prompt = f"""You are the Project Manager leading the 10-Agent Squad. Combine the architecture and security review into a final, highly polished, flawless response. Always address the user respectfully as Boss.
                
                Details:
                {audit_res}"""
                final_res = model.generate_content(pm_prompt).text

            # Append Final Collaborative Response
            st.session_state.messages.append({
                "role": "agent",
                "agent": "10-Agent Collaborative Squad (Lead: PM)",
                "content": final_res
            })
            
            st.rerun()
            
