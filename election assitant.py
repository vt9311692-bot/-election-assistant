import streamlit as st
import google.generativeai as genai
import os

# --- PAGE CONFIGURATION ---
st.set_page_config(page_title="ElectionGuide AI", page_icon="🗳️", layout="wide")

# Custom CSS for a professional look
st.markdown("""
    <style>
    .main { background-color: #f5f7f9; }
    .stChatMessage { border-radius: 15px; }
    .stButton>button { width: 100%; border-radius: 20px; background-color: #007bff; color: white; }
    </style>
    """, unsafe_allow_html=True)

# --- SYSTEM PROMPT ---
SYSTEM_PROMPT = """
You are ElectionGuide, an expert civic education assistant specializing in Indian election processes.
Your goal is to explain elections in a clear, structured, and accessible way.
- Friendly, approachable tone.
- Process: What → Why → How → Who is affected.
- Default context: India.
- No political bias. No speculation.
- End every response with a relevant follow-up question.
"""

# --- SIDEBAR SETUP ---
with st.sidebar:
    st.title("⚙️ Settings")
    api_key = st.text_input("Enter Gemini API Key", type="password")
    st.divider()
    st.markdown("### 📖 Quick Links")
    st.info("Official ECI Portal: [eci.gov.in](https://eci.gov.in)")
    st.info("Voter Portal: [voters.eci.gov.in](https://voters.eci.gov.in)")

# --- APP LOGIC ---
st.title("🗳️ ElectionGuide AI")
st.caption("Your friendly expert for democratic processes and voter education")

# Tabs for different features (This adds "Depth" to your project)
tab1, tab2 = st.tabs(["💬 AI Assistant", "✅ Eligibility Checker"])

with tab1:
    if not api_key:
        st.warning("Please enter your API Key in the sidebar to start chatting!")
    else:
        genai.configure(api_key=api_key)
        model = genai.GenerativeModel("gemini-1.5-flash", system_instruction=SYSTEM_PROMPT)

        # Initialize chat history
        if "messages" not in st.session_state:
            st.session_state.messages = []

        # Display chat history
        for message in st.session_state.messages:
            with st.chat_message(message["role"]):
                st.markdown(message["content"])

        # Chat input
        if prompt := st.chat_input("Ask me about voting, EVMs, or registration..."):
            st.session_state.messages.append({"role": "user", "content": prompt})
            with st.chat_message("user"):
                st.markdown(prompt)

            with st.chat_message("assistant"):
                chat = model.start_chat(history=[])
                response = chat.send_message(prompt)
                st.markdown(response.text)
                st.session_state.messages.append({"role": "assistant", "content": response.text})

with tab2:
    st.header("Check Your Voting Eligibility")
    st.write("Quickly find out if you are eligible to vote in India.")
    
    age = st.number_input("Enter your age", min_value=0, max_value=120, value=18)
    citizen = st.checkbox("Are you a citizen of India?")
    registered = st.checkbox("Are you registered in the electoral roll?")
    
    if st.button("Check Status"):
        if age >= 18 and citizen:
            if registered:
                st.success("🎉 You are fully eligible to vote! Make sure to carry your ID on polling day.")
            else:
                st.warning("⚠️ You are eligible, but you need to register first. Visit voters.eci.gov.in to fill Form 6.")
        else:
            st.error("❌ You are not currently eligible to vote. You must be a citizen of India and at least 18 years old.")