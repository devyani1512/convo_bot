import streamlit as st
from setup import agent

st.set_page_config(page_title=" Calendar Bot")
st.title(" Calendar Booking Agent")

if "messages" not in st.session_state:
    st.session_state.messages = []

user_input = st.chat_input("Ask me to book a meeting...")

if user_input:
    st.session_state.messages.append({"role": "user", "content": user_input})
    response = agent.run(user_input)
    st.session_state.messages.append({"role": "assistant", "content": response})

for msg in st.session_state.messages:
    st.chat_message(msg["role"]).write(msg["content"])
