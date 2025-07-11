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

# agent_setup.py
# agent_setup.py
# agent_setup.py
# agent_setup.py



# import os
# from langchain_openai import ChatOpenAI
# from langchain.agents import create_openai_functions_agent, AgentExecutor
# from langchain.tools import StructuredTool
# from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
# from langchain_core.messages import SystemMessage
# from pydantic import BaseModel

# from function.googlecalendar import (
#     book_event,
#     cancel_event,
#     check_availability,
#     check_schedule,
#     find_free_slots
# )

# # ✅ Use environment variable for OpenAI key
# llm = ChatOpenAI(
#     model="gpt-3.5-turbo",
#     temperature=0,
#     openai_api_key=os.getenv("OPENAI_API_KEY")  # ✅ correct keyword
# )

# # ✅ Tool Input Schemas
# class BookEventInput(BaseModel):
#     date: str
#     start_time: str
#     end_time: str
#     summary: str = "Meeting"
#     reminder: str | None = None

# class CancelEventInput(BaseModel):
#     summary: str
#     date: str

# class CheckAvailabilityInput(BaseModel):
#     date: str
#     start_time: str
#     end_time: str

# class CheckScheduleInput(BaseModel):
#     date: str

# class FindFreeSlotsInput(BaseModel):
#     date: str
#     duration_minutes: int = 60

# # ✅ Langchain Tools
# tools = [
#     StructuredTool.from_function(book_event, name="BookEvent", description="Book a meeting", args_schema=BookEventInput),
#     StructuredTool.from_function(cancel_event, name="CancelEvent", description="Cancel a meeting", args_schema=CancelEventInput),
#     StructuredTool.from_function(check_availability, name="CheckAvailability", description="Check free time slot", args_schema=CheckAvailabilityInput),
#     StructuredTool.from_function(check_schedule, name="CheckSchedule", description="Check meetings on a date", args_schema=CheckScheduleInput),
#     StructuredTool.from_function(find_free_slots, name="FindFreeSlots", description="Find open slots", args_schema=FindFreeSlotsInput),
# ]

# # ✅ Prompt + Agent
# prompt = ChatPromptTemplate.from_messages([
#     SystemMessage(content="You're a helpful assistant for Google Calendar. Always ask before booking."),
#     MessagesPlaceholder(variable_name="chat_history"),
#     MessagesPlaceholder(variable_name="input"),
#     MessagesPlaceholder(variable_name="agent_scratchpad")
# ])

# agent = create_openai_functions_agent(llm=llm, tools=tools, prompt=prompt)
# agent_executor = AgentExecutor(agent=agent, tools=tools, verbose=True)
