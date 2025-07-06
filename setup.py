from langchain.chat_models import ChatOpenAI
from langchain.agents import Tool
from langchain.agents import create_openai_functions_agent, AgentExecutor
from langchain.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain.schema.messages import SystemMessage

from function.googlecalendar import (
    book_event, BookEventInput,
    check_availability, CheckAvailabilityInput,
    check_schedule, CheckScheduleInput,
    find_free_slots, FindFreeSlotsInput
)

# 1. Define tools with args_schema
tools = [
    Tool.from_function(
        func=book_event,
        name="BookEvent",
        description="Book a meeting on a given date and time",
        args_schema=BookEventInput
    ),
    Tool.from_function(
        func=check_availability,
        name="CheckAvailability",
        description="Check if you're free during a time range on a certain day",
        args_schema=CheckAvailabilityInput
    ),
    Tool.from_function(
        func=check_schedule,
        name="CheckSchedule",
        description="See all your events on a specific day",
        args_schema=CheckScheduleInput
    ),
    Tool.from_function(
        func=find_free_slots,
        name="FindFreeSlots",
        description="Find free time slots on a given day",
        args_schema=FindFreeSlotsInput
    ),
]

# 2. Set up LLM
llm = ChatOpenAI(model="gpt-3.5-turbo", temperature=0)

# 3. Define prompt with correct input variables
prompt = ChatPromptTemplate.from_messages([
    SystemMessage(content=(
        "You are a helpful assistant that manages a user's Google Calendar. "
        "You must only respond based on actual calendar data and help with scheduling, availability checks, and booking."
    )),
    MessagesPlaceholder(variable_name="chat_history"),
    MessagesPlaceholder(variable_name="input"),
    MessagesPlaceholder(variable_name="agent_scratchpad")  # <- required!
])

# 4. Create agent and executor
agent = create_openai_functions_agent(
    llm=llm,
    tools=tools,
    prompt=prompt
)

agent_executor = AgentExecutor(
    agent=agent,
    tools=tools,
    verbose=True
)


