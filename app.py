import streamlit as st
from setup import agent

st.title("📅 Smart Google Calendar Assistant")
user_input = st.text_input("🗣️ You:", "")

if user_input:
    # Simple small talk responses
    greetings = ["hi", "hello", "hey", "how are you", "who are you"]
    user_input_lower = user_input.lower()

    if any(greet in user_input_lower for greet in greetings):
        if "how are you" in user_input_lower:
            st.write("🤖 I'm doing great! How can I assist you with your calendar today?")
        elif "who" in user_input_lower:
            st.write("👨‍💻 I'm your personal Google Calendar Assistant. You can ask me to book meetings, check availability, or suggest free slots.")
        else:
            st.write("👋 Hi there! What would you like me to do? (e.g. 'Book a meeting on Monday 3 to 4 PM')")
    else:
        with st.spinner("📡 Let me check your calendar..."):
            try:
                response = agent.run(user_input)
                st.success(response)
            except Exception as e:
                st.error(f"⚠️ Something went wrong: {e}")
