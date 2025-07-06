from google.oauth2 import service_account
from googleapiclient.discovery import build
import os, json
from datetime import datetime, timedelta
import pytz
import dateparser
from pydantic import BaseModel

creds_json = os.getenv("GOOGLE_CREDENTIALS_JSON")
info = json.loads(creds_json)
credentials = service_account.Credentials.from_service_account_info(
    info, scopes=["https://www.googleapis.com/auth/calendar"]
)
service = build("calendar", "v3", credentials=credentials)
CALENDAR_ID = "devyanisharmaa15@gmail.com"
TIMEZONE = "Asia/Kolkata"

class BookEventInput(BaseModel):
    date: str
    start_time: str
    end_time: str
    summary: str = "Meeting"

class CheckAvailabilityInput(BaseModel):
    date: str
    start_time: str
    end_time: str

class CheckScheduleInput(BaseModel):
    date: str

class FindFreeSlotsInput(BaseModel):
    date: str

def parse_date_time(date_str, time_str):
    return dateparser.parse(
        f"{date_str} {time_str}",
        settings={"TIMEZONE": TIMEZONE, "RETURN_AS_TIMEZONE_AWARE": True}
    )

def book_event(input: BookEventInput) -> str:
    start_dt = parse_date_time(input.date, input.start_time)
    end_dt = parse_date_time(input.date, input.end_time)

    if not start_dt or not end_dt or start_dt >= end_dt:
        return "❌ Invalid or unclear time range."

    body = {
        "summary": input.summary,
        "start": {"dateTime": start_dt.isoformat(), "timeZone": TIMEZONE},
        "end": {"dateTime": end_dt.isoformat(), "timeZone": TIMEZONE},
    }

    try:
        service.events().insert(calendarId=CALENDAR_ID, body=body).execute()
        return f"✅ Meeting booked on {input.date} from {input.start_time} to {input.end_time}."
    except Exception as e:
        return f"❌ Failed to book meeting: {e}"

def check_availability(input: CheckAvailabilityInput) -> str:
    start_dt = parse_date_time(input.date, input.start_time)
    end_dt = parse_date_time(input.date, input.end_time)

    if not start_dt or not end_dt:
        return "❌ Couldn't parse time range."

    events = service.events().list(
        calendarId=CALENDAR_ID,
        timeMin=start_dt.isoformat(),
        timeMax=end_dt.isoformat(),
        singleEvents=True,
        orderBy="startTime"
    ).execute().get("items", [])

    return "✅ You are free during that time." if not events else "🗓️ You have events during that time."

def check_schedule(input: CheckScheduleInput) -> str:
    start_dt = parse_date_time(input.date, "00:00")
    end_dt = parse_date_time(input.date, "23:59")

    if not start_dt or not end_dt:
        return "❌ Couldn't parse date."

    events = service.events().list(
        calendarId=CALENDAR_ID,
        timeMin=start_dt.isoformat(),
        timeMax=end_dt.isoformat(),
        singleEvents=True,
        orderBy="startTime"
    ).execute().get("items", [])

    if not events:
        return f"✅ No events scheduled for {input.date}."

    return "\n".join([
        f"{e['summary']} from {e['start']['dateTime']} to {e['end']['dateTime']}" for e in events
    ])

def find_free_slots(input: FindFreeSlotsInput, duration_minutes: int = 60) -> str:
    start_dt = parse_date_time(input.date, "00:00")
    end_dt = parse_date_time(input.date, "23:59")

    events = service.events().list(
        calendarId=CALENDAR_ID,
        timeMin=start_dt.isoformat(),
        timeMax=end_dt.isoformat(),
        singleEvents=True,
        orderBy="startTime"
    ).execute().get("items", [])

    busy_times = [(dateparser.parse(e["start"]["dateTime"]), dateparser.parse(e["end"]["dateTime"])) for e in events]
    busy_times.sort()

    current = start_dt
    free_slots = []

    for start, end in busy_times:
        if (start - current).total_seconds() >= duration_minutes * 60:
            free_slots.append(f"{current.strftime('%I:%M %p')} to {start.strftime('%I:%M %p')}")
        current = max(current, end)

    if (end_dt - current).total_seconds() >= duration_minutes * 60:
        free_slots.append(f"{current.strftime('%I:%M %p')} to {end_dt.strftime('%I:%M %p')}")

    return "\n".join(free_slots) if free_slots else f"❌ No free {duration_minutes}-minute slots on {input.date}."


# This file now uses natural language parsing entirely without Pydantic.




