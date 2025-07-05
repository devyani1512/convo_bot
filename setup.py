from langchain.chat_models import ChatOpenAI
from langchain.agents import Tool
from langchain.agents.openai_functions_agent.agent_token_buffer_memory import AgentTokenBufferMemory
from langchain.agents import create_openai_functions_agent
from langchain.agents.agent import AgentExecutor
from langchain.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain.schema.messages import SystemMessage

from function.googlecalendar import (
    book_event, BookEventInput,
    check_availability, CheckAvailabilityInput,
    check_schedule, CheckScheduleInput,
    find_free_slots, FindFreeSlotsInput
)

tools = [
    Tool.from_function(
        func=book_event,
        name="BookEvent",
        description="Book a meeting on a given day and time",
        args_schema=BookEventInput
    ),
    Tool.from_function(
        func=check_availability,
        name="CheckAvailability",
        description="Check if you are free at a certain time on a certain day",
        args_schema=CheckAvailabilityInput
    ),
    Tool.from_function(
        func=check_schedule,
        name="CheckSchedule",
        description="See all events scheduled on a given day",
        args_schema=CheckScheduleInput
    ),
    Tool.from_function(
        func=find_free_slots,
        name="FindFreeSlots",
        description="Find free time slots on a given day",
        args_schema=FindFreeSlotsInput
    )
]

# LLM
llm = ChatOpenAI(model="gpt-3.5-turbo", temperature=0)

# Prompt template for the agent
prompt = ChatPromptTemplate.from_messages([
    SystemMessage(content=(
        "You are a helpful Google Calendar assistant. "
        "You always answer using real calendar data. "
        "You can check availability, book events, find free slots, and list schedule for any day."
    )),
    MessagesPlaceholder(variable_name="chat_history"),
    MessagesPlaceholder(variable_name="input")
])

# Agent
agent = create_openai_functions_agent(
    llm=llm,
    tools=tools,
    prompt=prompt
)

# Agent executor
agent_executor = AgentExecutor(
    agent=agent,
    tools=tools,
    verbose=True
)


