from langchain.agents import Tool, initialize_agent
from langchain.chat_models import ChatOpenAI
from function.googlecalendar import book_event, check_availability, check_schedule, find_free_slots

# Define tools using explicit function calling (date, start_time, end_time, summary)
tools = [
    Tool.from_function(
        func=lambda date, start_time, end_time: check_availability(date, start_time, end_time),
        name="CheckAvailability",
        description="Checks if you're free during a time range like: date='Monday', start_time='3 PM', end_time='4 PM'."
    ),
    Tool.from_function(
        func=lambda date, start_time, end_time, summary="Meeting": book_event(date, start_time, end_time, summary),
        name="BookEvent",
        description="Books a meeting with a date, start_time, and end_time. For example: date='Friday', start_time='2 PM', end_time='3 PM'."
    ),
    Tool.from_function(
        func=lambda date: check_schedule(date),
        name="CheckSchedule",
        description="Checks your schedule on a specific date like 'today', 'tomorrow', '9th July', or 'Wednesday'."
    ),
    Tool.from_function(
        func=lambda date: find_free_slots(date),
        name="FindFreeSlots",
        description="Finds free time slots on a given date like 'Monday' or '9th July'."
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
