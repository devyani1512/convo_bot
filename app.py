import streamlit as st
from setup import agent
import re

st.set_page_config(page_title="Google Calendar Assistant", page_icon="📅")
st.title("📅 Google Calendar Assistant")
st.markdown("_Ask anything like:_")
st.markdown("- **Book a meeting on Monday from 2 PM to 3 PM**")
st.markdown("- **Am I free on 9th July from 11 AM to 12 PM?**")
st.markdown("- **What's my schedule tomorrow?**")
st.markdown("- **Find free slots on Saturday**")

user_input = st.text_input("You:", "")

if user_input:
    # Conversational fallback handling
    greetings = ["hi", "hello", "hey", "how are you", "who are you"]
    if any(greet in user_input.lower() for greet in greetings):
        if "how are you" in user_input.lower():
            st.write("🤖 I'm great, thanks for asking! How can I help you with your calendar?")
        elif "who" in user_input.lower():
            st.write("🧠 I’m your smart calendar assistant, connected to your real Google Calendar.")
        else:
            st.write("👋 Hi! How can I help you schedule or check something?")
    else:
        try:
            with st.spinner("🤔 Thinking..."):
                response = agent.run(user_input)
            st.success(response)
        except Exception as e:
            st.error(f"⚠️ Something went wrong: {e}")
