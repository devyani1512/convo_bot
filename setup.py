from langchain.chat_models import ChatOpenAI
from langchain.agents import Tool, create_openai_functions_agent, AgentExecutor
from langchain.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain.schema.messages import SystemMessage

from function.googlecalendar import (
    book_event, BookEventInput,
    check_availability, CheckAvailabilityInput,
    check_schedule, CheckScheduleInput,
    find_free_slots, FindFreeSlotsInput
)

tools = [
    Tool.from_function(func=book_event, name="BookEvent", description="Book a meeting", args_schema=BookEventInput),
    Tool.from_function(func=check_availability, name="CheckAvailability", description="Check availability", args_schema=CheckAvailabilityInput),
    Tool.from_function(func=check_schedule, name="CheckSchedule", description="See daily events", args_schema=CheckScheduleInput),
    Tool.from_function(func=find_free_slots, name="FindFreeSlots", description="Find free time", args_schema=FindFreeSlotsInput),
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



