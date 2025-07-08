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
import streamlit as st
from agent_setup import agent_executor
from langchain.schema import HumanMessage
import os, json
from google_auth_oauthlib.flow import Flow

st.set_page_config(page_title="Google Calendar Assistant", page_icon="📅")
st.title("📅 Google Calendar Assistant")

# Google OAuth login
if "google_token" not in st.session_state:
    config_info = json.loads(os.getenv("CLIENT_CONFIG_JSON"))
    flow = Flow.from_client_config(
        client_config=config_info,
        scopes=["https://www.googleapis.com/auth/calendar"],
        redirect_uri=os.getenv("https://convo-bot-p5ex.onrender.com", "http://localhost:8501")
    )

    auth_url, _ = flow.authorization_url(prompt="consent")
    st.write("🔐 Please [login with Google](%s) to continue." % auth_url)
else:
    user_input = st.text_input("You:", "")
    if user_input:
        with st.spinner("Thinking..."):
            try:
                result = agent_executor.invoke({
                    "input": [HumanMessage(content=user_input)],
                    "chat_history": []
                })
                st.success(result["output"])
            except Exception as e:
                st.error(f"⚠️ {e}")
