from langchain_community.chat_models import ChatOpenAI
from langchain.agents import initialize_agent, Tool
from function.googlecalendar import check_availability_natural, book_event_natural, check_schedule_day
from dotenv import load_dotenv
import os

load_dotenv()
openai_api_key = os.getenv("OPENAI_API_KEY")

llm = ChatOpenAI(temperature=0, openai_api_key=openai_api_key)

tools = [
    Tool(
        name="CheckAvailability",
        func=check_availability_natural,
        description="Check if you are free at a given time range like '3 PM to 4 PM today'."
    ),
    Tool(
        name="BookMeetingNatural",
        func=book_event_natural,
        description="Book a meeting. Example: 'today from 3 PM to 4 PM', 'tomorrow 10 AM to 11 AM'."
    ),
    Tool(
        name="DaySchedule",
        func=check_schedule_day,
        description="Check your schedule for a specific day. Example: 'today', 'tomorrow', 'Saturday'."
    ),
]

agent = initialize_agent(tools, llm, agent_type="openai-functions", handle_parsing_errors=True)

