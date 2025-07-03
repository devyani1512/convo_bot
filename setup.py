from langchain.agents import Tool, initialize_agent
from langchain_community.chat_models import ChatOpenAI  

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
        description=(
            "Use this tool to check if the calendar is free during a specific time range, "
            "such as '3 PM to 4 PM today', '1 PM to 2 PM tomorrow', etc."
        )
    ),
    Tool.from_function(
        func=book_event_natural,
        name="BookEvent",
        description=(
            "Use this to book a meeting using a natural time range like "
            "'10 AM to 11 AM on Friday', '1 PM to 2 PM today', etc."
        )
    ),
    Tool.from_function(
        func=check_schedule_day,
        name="CheckSchedule",
        description="Use this to view calendar events on a given day like 'today', 'tomorrow', or 'Monday'."
    ),
    Tool.from_function(
        func=find_free_slots,
        name="FindFreeSlots",
        description="Use this to find available time slots on a specific day like 'Saturday' or 'next Tuesday'."
    ),
]


llm = ChatOpenAI(
    model="gpt-3.5-turbo",  
    temperature=0,
    max_tokens=1000
)


agent = initialize_agent(
    tools=tools,
    llm=llm,
    agent_type="openai-functions",  
    verbose=True,
    handle_parsing_errors=True,
)
