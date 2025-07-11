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
# 📁 File: app.py
import streamlit as st
from openai import OpenAI
import os
import json

from function.googlecalendar import (
    book_event,
    cancel_event,
    check_availability,
    check_schedule,
    find_free_slots
)

# ✅ Setup
st.set_page_config(page_title="📅 Google Calendar Assistant", page_icon="📅")
st.title("📅 Google Calendar Assistant")

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

# ✅ Input from user
user_input = st.chat_input("You:")
if user_input:
    st.session_state.chat_history.append({"role": "user", "content": user_input})

    # ✅ Define available functions (OpenAI-style)
    function_definitions = [
        {
            "name": "book_event",
            "description": "Book a calendar event.",
            "parameters": {
                "type": "object",
                "properties": {
                    "date": {"type": "string"},
                    "start_time": {"type": "string"},
                    "end_time": {"type": "string"},
                    "summary": {"type": "string"},
                    "reminder": {"type": "string"}
                },
                "required": ["date", "start_time", "end_time"]
            }
        },
        {
            "name": "cancel_event",
            "description": "Cancel a calendar event.",
            "parameters": {
                "type": "object",
                "properties": {
                    "summary": {"type": "string"},
                    "date": {"type": "string"}
                },
                "required": ["summary", "date"]
            }
        },
        {
            "name": "check_availability",
            "description": "Check if there are any events in a time range.",
            "parameters": {
                "type": "object",
                "properties": {
                    "date": {"type": "string"},
                    "start_time": {"type": "string"},
                    "end_time": {"type": "string"}
                },
                "required": ["date", "start_time", "end_time"]
            }
        },
        {
            "name": "check_schedule",
            "description": "Show all events on a particular date.",
            "parameters": {
                "type": "object",
                "properties": {
                    "date": {"type": "string"}
                },
                "required": ["date"]
            }
        },
        {
            "name": "find_free_slots",
            "description": "Find free slots on a day for a given duration.",
            "parameters": {
                "type": "object",
                "properties": {
                    "date": {"type": "string"},
                    "duration_minutes": {"type": "integer"}
                },
                "required": ["date"]
            }
        }
    ]

    with st.spinner("Thinking..."):
        try:
            response = client.chat.completions.create(
                model="gpt-4",
                messages=st.session_state.chat_history,
                functions=function_definitions,
                function_call="auto"
            )

            message = response.choices[0].message

            # ✅ Handle function call
            if message.function_call:
                fn_name = message.function_call.name
                args = json.loads(message.function_call.arguments)

                fn_map = {
                    "book_event": book_event,
                    "cancel_event": cancel_event,
                    "check_availability": check_availability,
                    "check_schedule": check_schedule,
                    "find_free_slots": find_free_slots
                }

                result = fn_map[fn_name](**args)

                st.session_state.chat_history.append({
                    "role": "function",
                    "name": fn_name,
                    "content": result
                })
                st.success(result)

            else:
                # Assistant reply
                content = message.content
                st.session_state.chat_history.append({"role": "assistant", "content": content})
                st.success(content)

        except Exception as e:
            st.error(f"⚠️ Error: {e}")
