
import streamlit as st
from setup import agent

st.title("📅 Google Calendar Assistant")
user_input = st.text_input("You:", "")

if user_input:
    # Respond to greetings and small talk directly
    greetings = ["hi", "hello", "hey", "how are you", "who are you"]
    if any(greet in user_input.lower() for greet in greetings):
        if "how are you" in user_input.lower():
            st.write("🤖 I'm doing great, thanks for asking! How can I help you with your calendar?")
        elif "who" in user_input.lower():
            st.write("🧠 I’m your smart calendar assistant, connected to your actual Google Calendar.")
        else:
            st.write("👋 Hi! How can I help you schedule or check something?")
    else:
        try:
            with st.spinner("Thinking..."):
                response = agent.run(user_input)
            st.success(response)
        except Exception as e:
            st.error(f"⚠️ Oops: {str(e)}")
