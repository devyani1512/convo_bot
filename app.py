# import streamlit as st
# from setup import agent_executor
# from langchain.schema import HumanMessage

# st.set_page_config(page_title="Google Calendar Assistant", page_icon="📅")
# st.title("📅 Google Calendar Assistant")

# user_input = st.text_input("You:", "")

# if user_input:
#     greetings = ["hi", "hello", "hey", "how are you", "who are you"]
#     lower_input = user_input.lower()
#     if any(greet in lower_input for greet in greetings):
#         if "how are you" in lower_input:
#             st.write("🤖 I'm great, thanks! What can I help you schedule today?")
#         elif "who" in lower_input:
#             st.write("🧠 I’m your Google Calendar assistant, ready to help you manage your schedule.")
#         else:
#             st.write("👋 Hi! How can I assist with your calendar?")
#     else:
#         try:
#             with st.spinner("Working..."):
#                 result = agent_executor.invoke({
#                     "input": [HumanMessage(content=user_input)],
#                     "chat_history": []
#                 })
#             st.success(result["output"])
#         except Exception as e:
#             st.error(f"⚠️ Something went wrong: {e}")

# app.py
# app.py
import streamlit as st
from agent_setup import agent_executor
from langchain_core.messages import HumanMessage

st.set_page_config(page_title="\ud83d\udcc5 Google Calendar Assistant", page_icon="\ud83d\udcc5")
st.title("\ud83d\udcc5 Google Calendar Assistant")

if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

user_input = st.chat_input("You:")
if user_input:
    greetings = ["hi", "hello", "hey", "how are you", "who are you"]
    lower_input = user_input.lower()
    if any(greet in lower_input for greet in greetings):
        if "how are you" in lower_input:
            st.write("\ud83e\udd16 I'm great, thanks! What can I help you schedule today?")
        elif "who" in lower_input:
            st.write("\ud83e\udde0 I’m your Google Calendar assistant, ready to help you manage your schedule.")
        else:
            st.write("\ud83d\udc4b Hi! How can I assist with your calendar?")
    else:
        with st.spinner("Thinking..."):
            try:
                st.session_state.chat_history.append(HumanMessage(content=user_input))
                result = agent_executor.invoke({
                    "input": [HumanMessage(content=user_input)],
                    "chat_history": st.session_state.chat_history
                })
                st.success(result["output"])
            except Exception as e:
                st.error(f"\u26a0\ufe0f Error: {e}")
