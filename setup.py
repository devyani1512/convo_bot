from langchain.agents import Tool, initialize_agent
from langchain.chat_models import ChatOpenAI
from function.googlecalendar import (
    check_availability,
    book_event,
    check_schedule,
    find_free_slots
)

tools = [
    Tool.from_function(
        func=check_availability,
        name="CheckAvailability",
        description="Check if you're free on a certain date and time. Inputs: date (e.g. 'Monday'), start_time (e.g. '2 PM'), end_time (e.g. '3 PM')."
    ),
    Tool.from_function(
        func=book_event,
        name="BookEvent",
        description="Book a calendar event. Inputs: date (e.g. '9th July'), start_time (e.g. '3 PM'), end_time (e.g. '4 PM')."
    ),
    Tool.from_function(
        func=check_schedule,
        name="CheckSchedule",
        description="Check your schedule for a given day. Input: date (e.g. 'today', 'tomorrow', 'Saturday')."
    ),
    Tool.from_function(
        func=find_free_slots,
        name="FindFreeSlots",
        description="Find free time slots on a given date. Inputs: date (e.g. 'Monday'), duration_minutes (e.g. 60)."
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
