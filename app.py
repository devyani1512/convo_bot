# app.py
import streamlit as st
from setup import agent_executor

st.title("📅 Google Calendar Assistant")
user_input = st.text_input("You:", "")

if user_input:
    greetings = ["hi", "hello", "hey", "how are you", "who are you"]
    lower_input = user_input.lower()
    if any(greet in lower_input for greet in greetings):
        if "how are you" in lower_input:
            st.write("🤖 I'm great, thanks! What can I help you schedule today?")
        elif "who" in lower_input:
            st.write("🧠 I’m your Google Calendar assistant, ready to help you manage your schedule.")
        else:
            st.write("👋 Hi! How can I assist with your calendar?")
    else:
        try:
            with st.spinner("Working..."):
                response = agent_executor.invoke({"input": user_input})
            st.success(response["output"])
        except Exception as e:
            st.error(f"⚠️ Something went wrong: {e}")

