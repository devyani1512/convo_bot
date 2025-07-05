import streamlit as st
from setup import agent

st.set_page_config(page_title="Google Calendar Assistant", page_icon="📅")
st.title("📅 Smart Google Calendar Assistant")

user_input = st.text_input("You:", "")

if user_input:
    # Handle small talk or greetings
    greetings = ["hi", "hello", "hey", "how are you", "who are you"]
    user_lower = user_input.lower()

    if any(greet in user_lower for greet in greetings):
        if "how are you" in user_lower:
            st.write("🤖 I'm doing great! Thanks for asking. How can I help with your calendar?")
        elif "who" in user_lower:
            st.write("🧠 I’m your AI calendar assistant, here to schedule, check availability, and help you plan!")
        else:
            st.write("👋 Hi! What would you like to do with your calendar?")
    else:
        try:
            with st.spinner("Thinking..."):
                response = agent.run(user_input)
            st.success(response)
        except Exception as e:
            st.error(f"⚠️ Something went wrong: {e}")

