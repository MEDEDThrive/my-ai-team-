import streamlit as st
import google.generativeai as genai

# Page Configuration for Cyberpunk/Dark Theme
st.set_page_config(
    page_title="My AI Team - Boss Dashboard",
    page_icon="⚡",
    layout="centered"
)

# Custom Cyberpunk & WhatsApp Dark Theme CSS
st.markdown("""
    <style>
    .stApp {
        background-color: #0b141a;
        color: #e9edef;
    }
    .chat-bubble-user {
        background-color: #005c4b;
        color: #e9edef;
        padding: 12px 16px;
        border-radius: 10px 0px 10px 10px;
        margin: 8px 0;
        max-width: 85%;
        float: right;
        clear: both;
        box-shadow: 0 0 10px rgba(0, 255, 128, 0.2);
    }
    .chat-bubble-agent {
        background-color: #202c33;
        color: #e9edef;
        padding: 12px 16px;
        border-radius: 0px 10px 10px 10px;
        margin: 8px 0;
        max-width: 85%;
        float: left;
        clear: both;
        border-left: 4px solid #00ff88;
        box-shadow: 0 0 10px rgba(0, 255, 136, 0.1);
    }
    .agent-title {
        font-size: 11px;
        color: #00ff88;
        font-weight: bold;
        margin-bottom: 4px;
        text-transform: uppercase;
    }
    </style>
""", unsafe_allow_html=True)

# Header Section
st.markdown("### ⚡ MULTI-AGENT COMMAND CENTER")
st.markdown("<p style='color: #8696a0; font-size: 14px;'>Welcome back, Boss. Your elite AI development team is online and ready.</p>", unsafe_allow_html=True)
st.markdown("---")

# Sidebar for API Key & System Status
with st.sidebar:
    st.markdown("### ⚙️ System Controls")
    api_key = st.text_input("Enter Gemini API Key", type="password")
    st.markdown("---")
    st.markdown("### 🤖 Active Squad")
    st.markdown("🟢 **Senior Developer** (Architect)")
    st.markdown("🟢 **Code Reviewer** (Optimizer)")
    st.markdown("👤 **Boss** (You)")

# Initialize Gemini API if Key is provided
if api_key:
    genai.configure(api_key=api_key)
    model = genai.GenerativeModel('gemini-1.5-flash')

# Initialize Chat History
if "messages" not in st.session_state:
    st.session_state.messages = []

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

# User Input Box
user_prompt = st.chat_input("Command your AI Team, Boss...")

if user_prompt:
    if not api_key:
        st.warning("⚠️ Please enter your Gemini API Key in the sidebar first, Boss!")
    else:
        # Append User Message
        st.session_state.messages.append({"role": "user", "content": user_prompt})
        
        # Step 1: Senior Developer Drafts the Solution
        with st.spinner("Senior Developer is crafting the technical architecture..."):
            dev_prompt = f"""You are an elite Senior Developer working for Boss. 
            Address the user as Boss. Provide a robust, clean technical solution or code for this request: {user_prompt}"""
            dev_response = model.generate_content(dev_prompt).text

        # Step 2: Code Reviewer Refines and Optimizes it
        with st.spinner("Code Reviewer is auditing and optimizing the solution..."):
            reviewer_prompt = f"""You are a strict Code Reviewer and Quality Assurance expert working for Boss. 
            Review the following solution written by the Senior Developer for Boss. Fix any bugs, improve efficiency, 
            and present the final polished version clearly. Always address the user as Boss.
            
            Solution to review:
            {dev_response}"""
            final_response = model.generate_content(reviewer_prompt).text

        # Append Agent Final Response to History
        st.session_state.messages.append({
            "role": "agent", 
            "agent": "Senior Dev & Code Reviewer (Collab)", 
            "content": final_response
        })
        
        st.rerun()
        
