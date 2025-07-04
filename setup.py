from langchain.agents import Tool, initialize_agent
from langchain.chat_models import ChatOpenAI
from function.googlecalendar import (
    check_availability_natural,
    book_event_natural,
    check_schedule_day,
    find_free_slots,
)

tools = [
    Tool.from_function(
        func=check_availability_natural,
        name="CheckAvailability",
        description="Checks if you're free during a time range like '3 PM to 4 PM on 9th July' or 'tomorrow from 2 to 3 PM'."
    ),
    Tool.from_function(
        func=book_event_natural,
        name="BookEvent",
        description="Books a meeting using a time range like '9th July from 3 PM to 4 PM'."
    ),
    Tool.from_function(
        func=check_schedule_day,
        name="CheckSchedule",
        description="Checks your schedule on a specific day like 'today', 'tomorrow', or a date like '9th July'."
    ),
    Tool.from_function(
        func=find_free_slots,
        name="FindFreeSlots",
        description="Finds available time slots on a specific day like '9th July' or 'Monday'."
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

