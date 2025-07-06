from langchain.chat_models import ChatOpenAI
from langchain.agents import StructuredTool, create_openai_functions_agent, AgentExecutor
from langchain.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain.schema.messages import SystemMessage

from function.googlecalendar import (
    book_event, BookEventInput,
    check_availability, CheckAvailabilityInput,
    check_schedule, CheckScheduleInput,
    find_free_slots, FindFreeSlotsInput
)
tools = [
    StructuredTool.from_function(
        func=book_event,
        name="BookEvent",
        description="Book a meeting with date, start_time, end_time, and optional summary.",
        args_schema=BookEventInput
    ),
    StructuredTool.from_function(
        func=check_availability,
        name="CheckAvailability",
        description="Check if you are available on a given date/time range.",
        args_schema=CheckAvailabilityInput
    ),
    StructuredTool.from_function(
        func=check_schedule,
        name="CheckSchedule",
        description="Get the full schedule for a specific day.",
        args_schema=CheckScheduleInput
    ),
    StructuredTool.from_function(
        func=find_free_slots,
        name="FindFreeSlots",
        description="Find free time slots on a day.",
        args_schema=FindFreeSlotsInput
    ),
]


llm = ChatOpenAI(model="gpt-3.5-turbo", temperature=0)

prompt = ChatPromptTemplate.from_messages([
    SystemMessage(content="You are a helpful assistant for Google Calendar."),
    MessagesPlaceholder(variable_name="chat_history"),
    MessagesPlaceholder(variable_name="input"),
    MessagesPlaceholder(variable_name="agent_scratchpad")
])

agent = create_openai_functions_agent(llm=llm, tools=tools, prompt=prompt)

agent_executor = AgentExecutor(agent=agent, tools=tools, verbose=True)



