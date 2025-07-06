# import streamlit as st
# from setup import agent_executor
# from langchain.schema import HumanMessage

# st.set_page_config(page_title="Google Calendar Assistant", page_icon="📅")
# st.title("📅 Google Calendar Assistant")

# user_input = st.text_input("You:", "")

# if user_input:
#     greetings = ["hi", "hello", "hey", "how are you", "who are you"]
#     lower_input = user_input.lower()
#     if any(greet in lower_input for greet in greetings):
#         if "how are you" in lower_input:
#             st.write("🤖 I'm great, thanks! What can I help you schedule today?")
#         elif "who" in lower_input:
#             st.write("🧠 I’m your Google Calendar assistant, ready to help you manage your schedule.")
#         else:
#             st.write("👋 Hi! How can I assist with your calendar?")
#     else:
#         try:
#             with st.spinner("Working..."):
#                 result = agent_executor.invoke({
#                     "input": [HumanMessage(content=user_input)],
#                     "chat_history": []
#                 })
#             st.success(result["output"])
#         except Exception as e:
#             st.error(f"⚠️ Something went wrong: {e}")
from flask import Flask, request, jsonify
from google.oauth2 import service_account
from googleapiclient.discovery import build
import os, json
from datetime import datetime
import pytz
import dateparser

app = Flask(__name__)

# --- Setup Google Calendar API ---
creds_json = os.getenv("GOOGLE_CREDENTIALS_JSON")
info = json.loads(creds_json)
credentials = service_account.Credentials.from_service_account_info(
    info, scopes=["https://www.googleapis.com/auth/calendar"]
)
service = build("calendar", "v3", credentials=credentials)

CALENDAR_ID = "devyanisharmaa15@gmail.com"
TIMEZONE = "Asia/Kolkata"

# --- Helpers ---
def parse_date_time(date_str, time_str):
    return dateparser.parse(
        f"{date_str} {time_str}",
        settings={"TIMEZONE": TIMEZONE, "RETURN_AS_TIMEZONE_AWARE": True}
    )

def parse_reminder_string(reminder_str: str) -> list[int]:
    if not reminder_str:
        return [15]
    reminder_str = reminder_str.lower()
    reminders = []
    if "hour" in reminder_str:
        hours = reminder_str.split("hour")[0].strip()
        if hours.isdigit():
            reminders.append(int(hours) * 60)
    if "minute" in reminder_str:
        if "and" in reminder_str:
            minutes = reminder_str.split("and")[-1]
        else:
            minutes = reminder_str.split("minute")[0]
        minutes = "".join(filter(str.isdigit, minutes))
        if minutes:
            reminders.append(int(minutes))
    return reminders or [15]

# --- Routes ---
@app.route("/book", methods=["POST"])
def book_event():
    data = request.json
    date = data.get("date")
    start_time = data.get("start_time")
    end_time = data.get("end_time")
    summary = data.get("summary", "Meeting")
    reminder = data.get("reminder")

    start_dt = parse_date_time(date, start_time)
    end_dt = parse_date_time(date, end_time)

    if not start_dt or not end_dt or start_dt >= end_dt:
        return jsonify({"status": "error", "message": "Invalid time range."}), 400

    overrides = [{"method": "popup", "minutes": m} for m in parse_reminder_string(reminder)]

    event = {
        "summary": summary,
        "start": {"dateTime": start_dt.isoformat(), "timeZone": TIMEZONE},
        "end": {"dateTime": end_dt.isoformat(), "timeZone": TIMEZONE},
        "reminders": {"useDefault": False, "overrides": overrides}
    }

    try:
        service.events().insert(calendarId=CALENDAR_ID, body=event).execute()
        return jsonify({"status": "success", "message": f"Meeting booked on {date} from {start_time} to {end_time}."})
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500

@app.route("/cancel", methods=["POST"])
def cancel_event():
    data = request.json
    summary = data.get("summary")
    date = data.get("date")

    start_dt = parse_date_time(date, "00:00")
    end_dt = parse_date_time(date, "23:59")

    try:
        events = service.events().list(
            calendarId=CALENDAR_ID,
            timeMin=start_dt.isoformat(),
            timeMax=end_dt.isoformat(),
            singleEvents=True,
            orderBy="startTime"
        ).execute().get("items", [])

        for event in events:
            if event.get("summary", "").lower() == summary.lower():
                service.events().delete(calendarId=CALENDAR_ID, eventId=event["id"]).execute()
                return jsonify({"status": "success", "message": f"Cancelled '{summary}' on {date}."})

        return jsonify({"status": "error", "message": f"No event titled '{summary}' found on {date}."}), 404
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500

@app.route("/availability", methods=["POST"])
def check_availability():
    data = request.json
    date = data.get("date")
    start_time = data.get("start_time")
    end_time = data.get("end_time")

    start_dt = parse_date_time(date, start_time)
    end_dt = parse_date_time(date, end_time)

    events = service.events().list(
        calendarId=CALENDAR_ID,
        timeMin=start_dt.isoformat(),
        timeMax=end_dt.isoformat(),
        singleEvents=True,
        orderBy="startTime"
    ).execute().get("items", [])

    free = not events
    return jsonify({"status": "success", "available": free})

@app.route("/schedule", methods=["POST"])
def check_schedule():
    data = request.json
    date = data.get("date")
    start_dt = parse_date_time(date, "00:00")
    end_dt = parse_date_time(date, "23:59")

    events = service.events().list(
        calendarId=CALENDAR_ID,
        timeMin=start_dt.isoformat(),
        timeMax=end_dt.isoformat(),
        singleEvents=True,
        orderBy="startTime"
    ).execute().get("items", [])

    result = [
        {
            "summary": e["summary"],
            "start": e["start"]["dateTime"],
            "end": e["end"]["dateTime"]
        }
        for e in events
    ]

    return jsonify({"status": "success", "events": result})

@app.route("/free-slots", methods=["POST"])
def find_free_slots():
    data = request.json
    date = data.get("date")
    duration_minutes = int(data.get("duration_minutes", 60))

    start_dt = parse_date_time(date, "00:00")
    end_dt = parse_date_time(date, "23:59")

    events = service.events().list(
        calendarId=CALENDAR_ID,
        timeMin=start_dt.isoformat(),
        timeMax=end_dt.isoformat(),
        singleEvents=True,
        orderBy="startTime"
    ).execute().get("items", [])

    busy = [(dateparser.parse(e["start"]["dateTime"]), dateparser.parse(e["end"]["dateTime"])) for e in events]
    busy.sort()

    current = start_dt
    free_slots = []

    for start, end in busy:
        if (start - current).total_seconds() >= duration_minutes * 60:
            free_slots.append(f"{current.strftime('%I:%M %p')} to {start.strftime('%I:%M %p')}")
        current = max(current, end)

    if (end_dt - current).total_seconds() >= duration_minutes * 60:
        free_slots.append(f"{current.strftime('%I:%M %p')} to {end_dt.strftime('%I:%M %p')}")

    return jsonify({
        "status": "success",
        "slots": free_slots or ["❌ No free slots for the requested duration."]
    })

# --- Run Server ---
if __name__ == "__main__":
    app.run(debug=True)
