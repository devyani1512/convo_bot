
from langchain.agents import Tool, initialize_agent
from langchain.chat_models import ChatOpenAI
from function.googlecalendar import (
    check_availability_natural,
    book_event_natural,
    check_schedule_day,
    find_free_slots
)


tools = [
    Tool.from_function(
        func=check_availability_natural,
        name="CheckAvailability",
        description="Checks if you're free during a time range like '3 PM to 4 PM today'."
    ),
    Tool.from_function(
        func=book_event_natural,
        name="BookEvent",
        description="Books a meeting using a time range like '3 PM to 4 PM today'."
    ),
    Tool.from_function(
        func=check_schedule_day,
        name="CheckSchedule",
        description="Checks your schedule on a day like 'today', 'tomorrow', or 'Saturday'."
    ),
    Tool.from_function(
        func=find_free_slots,
        name="FindFreeSlots",
        description="Finds free time slots on a given day like 'Saturday'."
    ),
]

# Use ChatOpenAI with GPT-3.5 (can be changed to gpt-4 if you have access)
llm = ChatOpenAI(temperature=0, model="gpt-3.5-turbo")

# Initialize the agent
agent = initialize_agent(
    tools=tools,
    llm=llm,
    agent_type="openai-functions",
    verbose=True,
    handle_parsing_errors=True,
)
