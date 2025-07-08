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
import json, os
from langchain.schema import HumanMessage
from setup import agent_executor
from google_auth_oauthlib.flow import Flow
from urllib.parse import urlencode

st.set_page_config(page_title="Google Calendar Assistant", page_icon="📅")
st.title("📅 Google Calendar Assistant")

CLIENT_CONFIG = json.loads(os.getenv("CLIENT_CONFIG_JSON"))
REDIRECT_URI = "https://your-app-name.onrender.com"  # set this to your Render domain

if "google_user_token_info" not in st.session_state:
    code = st.query_params.get("code")
    if code:
        flow = Flow.from_client_config(CLIENT_CONFIG, scopes=["https://www.googleapis.com/auth/calendar"], redirect_uri=REDIRECT_URI)
        flow.fetch_token(code=code)
        creds = flow.credentials
        st.session_state["google_user_token_info"] = json.loads(creds.to_json())
        st.experimental_rerun()
    else:
        auth_url, _ = Flow.from_client_config(
            CLIENT_CONFIG,
            scopes=["https://www.googleapis.com/auth/calendar"],
            redirect_uri=REDIRECT_URI
        ).authorization_url(prompt='consent')
        st.markdown(f"[🔑 Login with Google]({auth_url})")
        st.stop()

user_input = st.text_input("You:", "")
if user_input:
    if user_input.lower() in ["hi", "hello", "who are you"]:
        st.write("👋 Hello! I'm your personal calendar assistant.")
    else:
        with st.spinner("Thinking..."):
            try:
                result = agent_executor.invoke({
                    "input": [HumanMessage(content=user_input)],
                    "chat_history": []
                })
                st.success(result["output"])
            except Exception as e:
                st.error(f"❌ {e}")
