from langchain.chat_models import ChatOpenAI
from langchain.agents import initialize_agent, Tool
from function.googlecalender import check_availability, book_event, book_event_natural
import os
from dotenv import load_dotenv

load_dotenv()
openai_api_key = os.getenv("OPENAI_API_KEY")

llm = ChatOpenAI(temperature=0, openai_api_key=openai_api_key)

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
),Tool(
    name="BookMeetingNatural",
    func=book_event_natural,
    description="Use this to book a meeting using natural language. Example input: 'today from 3 PM to 4 PM', 'tomorrow 10 AM to 11 AM', etc."
)


]

agent = initialize_agent(tools, llm, agent_type="openai-functions")
