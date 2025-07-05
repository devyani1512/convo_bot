from langchain.agents import Tool, initialize_agent
from langchain.chat_models import ChatOpenAI
from function.googlecalendar import book_event, check_availability, check_schedule, find_free_slots

# Define tools with clear argument-based invocation
book_tool = Tool(
    name="BookEvent",
    func=lambda date, start_time, end_time: book_event(date, start_time, end_time),
    description="Books a meeting given a date like 'Monday' or '9th July', and a time range like '2 PM to 3 PM'. Requires three arguments: date, start_time, end_time."
)

availability_tool = Tool(
    name="CheckAvailability",
    func=lambda date, start_time, end_time: check_availability(date, start_time, end_time),
    description="Checks if you're free at a given date and time range. Example inputs: date='tomorrow', start_time='3 PM', end_time='4 PM'."
)

schedule_tool = Tool(
    name="CheckSchedule",
    func=lambda date: check_schedule(date),
    description="Checks your schedule for a day like 'today', 'tomorrow', or 'Saturday'. Takes one argument: date."
)

free_slots_tool = Tool(
    name="FindFreeSlots",
    func=lambda date: find_free_slots(date),
    description="Finds available time slots on a given day like 'Friday' or '9th July'. Takes one argument: date."
)

tools = [book_tool, availability_tool, schedule_tool, free_slots_tool]

llm = ChatOpenAI(temperature=0, model="gpt-3.5-turbo")

agent = initialize_agent(
    tools=tools,
    llm=llm,
    agent_type="openai-functions",
    verbose=True,
    handle_parsing_errors=True,
)

