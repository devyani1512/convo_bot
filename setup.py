from langchain.agents import Tool

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
        description="Checks what is scheduled on a day like 'today', 'tomorrow', or 'Saturday'."
    ),
    Tool.from_function(
        func=find_free_slots,
        name="FindFreeSlots",
        description="Finds free slots on a day. Input example: 'Saturday', 'tomorrow'."
    ),
]


