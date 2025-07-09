# from langchain.chat_models import ChatOpenAI
# from langchain.agents import create_openai_functions_agent, AgentExecutor
# from langchain.prompts import ChatPromptTemplate, MessagesPlaceholder
# from langchain.schema.messages import SystemMessage
# from langchain.tools import StructuredTool

# from function.googlecalendar import (
#     book_event,
#     check_availability,
#     check_schedule,
#     find_free_slots
# )

# # Define tools
# tools = [
#     StructuredTool.from_function(
#         func=book_event,
#         name="BookEvent",
#         description="Book a meeting with date, start_time, end_time, and optional summary."
#     ),
#     StructuredTool.from_function(
#         func=check_availability,
#         name="CheckAvailability",
#         description="Check if you are available on a given date/time range."
#     ),
#     StructuredTool.from_function(
#         func=check_schedule,
#         name="CheckSchedule",
#         description="Get the full schedule for a specific day."
#     ),
#     StructuredTool.from_function(
#         func=find_free_slots,
#         name="FindFreeSlots",
#         description="Find free time slots on a day."
#     ),
# ]

# # LLM setup
# llm = ChatOpenAI(model="gpt-3.5-turbo", temperature=0)

# # Prompt template
# prompt = ChatPromptTemplate.from_messages([
#     SystemMessage(content="You are a helpful assistant for Google Calendar."),
#     MessagesPlaceholder(variable_name="chat_history"),
#     MessagesPlaceholder(variable_name="input"),
#     MessagesPlaceholder(variable_name="agent_scratchpad")
# ])

# # Agent setup
# agent = create_openai_functions_agent(llm=llm, tools=tools, prompt=prompt)

# # Executor
# agent_executor = AgentExecutor(agent=agent, tools=tools, verbose=True)



# from langchain.chat_models import ChatOpenAI
# from langchain.agents import create_openai_functions_agent, AgentExecutor
# from langchain.prompts import ChatPromptTemplate, MessagesPlaceholder
# from langchain.schema.messages import SystemMessage
# from langchain.tools import StructuredTool

# from function.googlecalendar import (
#     book_event,
#     cancel_event,
#     check_availability,
#     check_schedule,
#     find_free_slots
# )

# # Define tools
# tools = [
#     StructuredTool.from_function(
#         func=book_event,
#         name="BookEvent",
#         description="Book a meeting with date, start_time, end_time, optional summary, and optional natural reminder string like '15 minutes' or '1 hour and 15 minutes'."
#     ),
#     StructuredTool.from_function(
#         func=cancel_event,
#         name="CancelEvent",
#         description="Cancel a calendar event by providing its title (summary) and date. Example: 'Cancel Standup on July 10th'"
#     ),
#     StructuredTool.from_function(
#         func=check_availability,
#         name="CheckAvailability",
#         description="Check if you are available on a given date/time range."
#     ),
#     StructuredTool.from_function(
#         func=check_schedule,
#         name="CheckSchedule",
#         description="Get the full schedule for a specific day."
#     ),
#     StructuredTool.from_function(
#         func=find_free_slots,
#         name="FindFreeSlots",
#         description="Find free time slots on a day."
#     ),
# ]

# # LLM setup
# llm = ChatOpenAI(model="gpt-3.5-turbo", temperature=0)

# # Prompt template
# prompt = ChatPromptTemplate.from_messages([
#     SystemMessage(content="You are a helpful assistant for Google Calendar. Always ask for confirmation before booking."),
#     MessagesPlaceholder(variable_name="chat_history"),
#     MessagesPlaceholder(variable_name="input"),
#     MessagesPlaceholder(variable_name="agent_scratchpad")
# ])

# # Agent setup
# agent = create_openai_functions_agent(llm=llm, tools=tools, prompt=prompt)

# # Executor
# agent_executor = AgentExecutor(agent=agent, tools=tools, verbose=True)

# from langchain.chat_models import ChatOpenAI
# from langchain.agents import create_openai_functions_agent, AgentExecutor
# from langchain.prompts import ChatPromptTemplate, MessagesPlaceholder
# from langchain.schema.messages import SystemMessage
# from langchain.tools import StructuredTool

# from function.googlecalendar import (
#     book_event,
#     check_availability,
#     check_schedule,
#     find_free_slots
# )

# # Define tools
# tools = [
#     StructuredTool.from_function(
#         func=book_event,
#         name="BookEvent",
#         description="Book a meeting with date, start_time, end_time, and optional summary."
#     ),
#     StructuredTool.from_function(
#         func=check_availability,
#         name="CheckAvailability",
#         description="Check if you are available on a given date/time range."
#     ),
#     StructuredTool.from_function(
#         func=check_schedule,
#         name="CheckSchedule",
#         description="Get the full schedule for a specific day."
#     ),
#     StructuredTool.from_function(
#         func=find_free_slots,
#         name="FindFreeSlots",
#         description="Find free time slots on a day."
#     ),
# ]

# # LLM setup
# llm = ChatOpenAI(model="gpt-3.5-turbo", temperature=0)

# # Prompt template
# prompt = ChatPromptTemplate.from_messages([
#     SystemMessage(content="You are a helpful assistant for Google Calendar."),
#     MessagesPlaceholder(variable_name="chat_history"),
#     MessagesPlaceholder(variable_name="input"),
#     MessagesPlaceholder(variable_name="agent_scratchpad")
# ])

# # Agent setup
# agent = create_openai_functions_agent(llm=llm, tools=tools, prompt=prompt)

# # Executor
# agent_executor = AgentExecutor(agent=agent, tools=tools, verbose=True)



# from langchain.chat_models import ChatOpenAI
# from langchain.agents import create_openai_functions_agent, AgentExecutor
# from langchain.prompts import ChatPromptTemplate, MessagesPlaceholder
# from langchain.schema.messages import SystemMessage
# from langchain.tools import StructuredTool

# from function.googlecalendar import (
#     book_event,
#     cancel_event,
#     check_availability,
#     check_schedule,
#     find_free_slots
# )

# # Define tools
# tools = [
#     StructuredTool.from_function(
#         func=book_event,
#         name="BookEvent",
#         description="Book a meeting with date, start_time, end_time, optional summary, and optional natural reminder string like '15 minutes' or '1 hour and 15 minutes'."
#     ),
#     StructuredTool.from_function(
#         func=cancel_event,
#         name="CancelEvent",
#         description="Cancel a calendar event by providing its title (summary) and date. Example: 'Cancel Standup on July 10th'"
#     ),
#     StructuredTool.from_function(
#         func=check_availability,
#         name="CheckAvailability",
#         description="Check if you are available on a given date/time range."
#     ),
#     StructuredTool.from_function(
#         func=check_schedule,
#         name="CheckSchedule",
#         description="Get the full schedule for a specific day."
#     ),
#     StructuredTool.from_function(
#         func=find_free_slots,
#         name="FindFreeSlots",
#         description="Find free time slots on a day."
#     ),
# ]

# # LLM setup
# llm = ChatOpenAI(model="gpt-3.5-turbo", temperature=0)

# # Prompt template
# prompt = ChatPromptTemplate.from_messages([
#     SystemMessage(content="You are a helpful assistant for Google Calendar. Always ask for confirmation before booking."),
#     MessagesPlaceholder(variable_name="chat_history"),
#     MessagesPlaceholder(variable_name="input"),
#     MessagesPlaceholder(variable_name="agent_scratchpad")
# ])

# # Agent setup
# agent = create_openai_functions_agent(llm=llm, tools=tools, prompt=prompt)

# # Executor
# agent_executor = AgentExecutor(agent=agent, tools=tools, verbose=True)

# setup.py
import os
from langchain_community.chat_models import ChatOpenAI
# from langchain.agents.openai_functions_agent.base import OpenAIFunctionsAgent
# from langchain.agents import AgentExecutor
from langchain.agents import create_openai_functions_agent, AgentExecutor
from langchain.tools import Tool

from function.googlecalendar import (
    book_event,
    cancel_event,
    check_availability,
    check_schedule,
    find_free_slots
)

llm = ChatOpenAI(model="gpt-4", temperature=0)

tools = [
    Tool.from_function(book_event, name="book_event", description="Book an event."),
    Tool.from_function(cancel_event, name="cancel_event", description="Cancel an event."),
    Tool.from_function(check_availability, name="check_availability", description="Check availability."),
    Tool.from_function(check_schedule, name="check_schedule", description="Show day's schedule."),
    Tool.from_function(find_free_slots, name="find_free_slots", description="Find free time slots."),
]

# agent = OpenAIFunctionsAgent.from_llm_and_tools(llm=llm, tools=tools)
agent = create_openai_functions_agent(llm=llm, tools=tools, prompt=prompt)
agent_executor = AgentExecutor(agent=agent, tools=tools, verbose=True)

