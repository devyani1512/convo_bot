from langchain.agents import Tool, initialize_agent
from langchain.chat_models import ChatOpenAI
from langchain.tools import tool
from pydantic import BaseModel, Field

from function.googlecalendar import (
    book_event,
    check_availability,
    check_schedule,
    find_free_slots
)

# --- Define argument schemas ---
class BookEventArgs(BaseModel):
    date: str = Field(..., description="Date of the meeting (e.g. 'tomorrow' or '9th July')")
    start_time: str = Field(..., description="Start time (e.g. '3 PM')")
    end_time: str = Field(..., description="End time (e.g. '4 PM')")

class CheckAvailabilityArgs(BaseModel):
    date: str
    start_time: str
    end_time: str

class CheckScheduleArgs(BaseModel):
    date: str

class FreeSlotsArgs(BaseModel):
    date: str
    duration_minutes: int = 60

# --- Tools ---
tools = [
    Tool.from_function(
        func=book_event,
        name="BookEvent",
        description="Book a meeting on a given date and time.",
        args_schema=BookEventArgs
    ),
    Tool.from_function(
        func=check_availability,
        name="CheckAvailability",
        description="Check if you're free on a given date and time.",
        args_schema=CheckAvailabilityArgs
    ),
    Tool.from_function(
        func=check_schedule,
        name="CheckSchedule",
        description="Get your schedule for a given day.",
        args_schema=CheckScheduleArgs
    ),
    Tool.from_function(
        func=find_free_slots,
        name="FindFreeSlots",
        description="Find free slots on a given day.",
        args_schema=FreeSlotsArgs
    ),
]

llm = ChatOpenAI(temperature=0, model="gpt-3.5-turbo")

agent = initialize_agent(
    tools=tools,
    llm=llm,
    agent_type="openai-functions",
    verbose=True,
    handle_parsing_errors=True
)

