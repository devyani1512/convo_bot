import streamlit as st
from setup import agent_executor

st.set_page_config(page_title="🗓️ Google Calendar Assistant", layout="centered")
st.title("🧠 Google Calendar Assistant")

user_input = st.text_input("You:", placeholder="Ask me anything about your calendar...")

if user_input:
    greetings = ["hi", "hello", "hey", "how are you", "who are you"]
    if any(greet in user_input.lower() for greet in greetings):
        if "how are you" in user_input.lower():
            st.write("🤖 I'm doing great! How can I help you with your calendar?")
        elif "who" in user_input.lower():
            st.write("🧠 I'm your calendar assistant, powered by your actual Google Calendar.")
        else:
            st.write("👋 Hello! What can I do for you today?")
    else:
        try:
            with st.spinner("Thinking..."):
                response = agent_executor.run(user_input)
            st.success(response)
        except Exception as e:
            st.error(f"⚠️ Error: {str(e)}")

