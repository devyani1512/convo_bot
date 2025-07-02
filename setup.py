from dotenv import load_dotenv
import os

from langchain_community.chat_models import ChatOpenAI
from langchain.agents import initialize_agent, Tool

from function.googlecalendar import check_availability, book_event, book_event_natural

# Load .env variables
load_dotenv()
openai_api_key = os.getenv("OPENAI_API_KEY")

# LLM setup
llm = ChatOpenAI(temperature=0, openai_api_key=openai_api_key)

# Define tools
tools = [
    Tool(
        name="CheckAvailability",
        func=lambda x: str(check_availability()),
        description="Use this to check the next available time slots."
    ),
    Tool(
        name="BookEvent",
        func=lambda x: book_event("Meeting", *x.split(",")) if len(x.split(",")) == 2 else "❌ Error: Please provide start and end times separated by a comma.",
        description="Use this to book a meeting. Input format: start_time,end_time (ISO 8601 format)."
    ),
    Tool(
        name="BookMeetingNatural",
        func=lambda x: book_event_natural(x),
        description="Use this to book a meeting using natural language. Example: 'tomorrow from 4 PM to 5 PM'"
    )
]

# Initialize agent
agent = initialize_agent(tools, llm, agent_type="openai-functions")



