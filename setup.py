from langchain_community.chat_models import ChatOpenAI
from langchain.agents import initialize_agent, Tool
from function.googlecalendar import check_availability, book_event, book_event_natural
import os
from dotenv import load_dotenv

load_dotenv()
openai_api_key = os.getenv("OPENAI_API_KEY")

llm = ChatOpenAI(temperature=0, openai_api_key=openai_api_key)

tools = [
    Tool(
        name="CheckAvailability",
        func=lambda _: str(check_availability()),
        description="Use this to check the next available time slots."
    ),
    Tool(
        name="BookEvent",
        func=lambda x: book_event("Meeting", *x.split(",")) if len(x.split(",")) == 2 else "❌ Error: Provide start and end time in format: start,end (ISO 8601).",
        description="Use this to book a meeting. Input format: start_time,end_time (ISO 8601 format)."
    ),
    Tool(
        name="BookMeetingNatural",
        func=book_event_natural,
        description="Use this to book a meeting using natural language. Example input: 'tomorrow 3pm to 4pm'."
    )
]

agent = initialize_agent(tools, llm, agent_type="openai-functions")


