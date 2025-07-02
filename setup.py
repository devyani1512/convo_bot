import os
import json
from dotenv import load_dotenv
from google.oauth2 import service_account
from googleapiclient.discovery import build
from langchain.chat_models import ChatOpenAI
from langchain.agents import initialize_agent, Tool
from function.googlecalendar import check_availability, book_event, book_event_natural

# Load .env environment variables
load_dotenv()

# Set up OpenAI
openai_api_key = os.getenv("OPENAI_API_KEY")
llm = ChatOpenAI(temperature=0, openai_api_key=openai_api_key)

# Set up Google Calendar credentials from minified JSON
creds_json = os.getenv("GOOGLE_CREDENTIALS_JSON")
info = json.loads(creds_json)
credentials = service_account.Credentials.from_service_account_info(info)
service = build("calendar", "v3", credentials=credentials)

# Pass the authorized service to your functions (if needed)
# You may update your functions to accept `service` as a parameter if needed

# Define tools
tools = [
    Tool(
        name="CheckAvailability",
        func=lambda x: str(check_availability(service)),
        description="Use this to check the next available time slots."
    ),
    Tool(
        name="BookEvent",
        func=lambda x: book_event("Meeting", *x.split(","), service=service) if len(x.split(",")) == 2 else "❌ Error: Please provide start and end times separated by a comma.",
        description="Use this to book a meeting. Input format: start_time,end_time (ISO 8601 format)."
    ),
    Tool(
        name="BookMeetingNatural",
        func=lambda x: book_event_natural(x, service),
        description="Use this to book a meeting using natural language. Example input: 'today from 3 PM to 4 PM', 'tomorrow 10 AM to 11 AM', etc."
    )
]

# Initialize agent
agent = initialize_agent(tools, llm, agent_type="openai-functions")

