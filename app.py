
import streamlit as st
from setup import agent

st.set_page_config(page_title="AI Calendar Assistant")
st.title("AI Calendar Scheduler")


user_input = st.text_input("Ask me to schedule/check a meeting:", placeholder="e.g. Book a meeting today from 2 PM to 3 PM")


if st.button("Submit") and user_input:
    with st.spinner("Thinking..."):
        try:
            response = agent.run(user_input)
            st.success(response)
        except Exception as e:
            st.error(f" Error: {str(e)}")

