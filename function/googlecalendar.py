from google.oauth2 import service_account
from googleapiclient.discovery import build
import json, os
from datetime import datetime, timedelta
import pytz
import dateparser
from typing import Optional
from pydantic import BaseModel, Field

creds_json = os.getenv("GOOGLE_CREDENTIALS_JSON")
info = json.loads(creds_json)
credentials = service_account.Credentials.from_service_account_info(
    info, scopes=["https://www.googleapis.com/auth/calendar"]
)
service = build("calendar", "v3", credentials=credentials)
CALENDAR_ID = "devyanisharmaa15@gmail.com"
TIMEZONE = "Asia/Kolkata"

def parse_datetime_flexible(date_str, time_str):
    dt = dateparser.parse(
        f"{date_str} {time_str}",
        settings={"TIMEZONE": TIMEZONE, "RETURN_AS_TIMEZONE_AWARE": True}
    )
    return dt

class BookEventInput(BaseModel):
    date: str = Field(..., description="The day or date like 'Monday' or '9th July'")
    start_time: str = Field(..., description="Start time like '2 PM'")
    end_time: str = Field(..., description="End time like '3 PM'")
    summary: Optional[str] = Field("Meeting", description="Title of the meeting")

def book_event(inputs: BookEventInput) -> str:
    start_dt = parse_datetime_flexible(inputs.date, inputs.start_time)
    end_dt = parse_datetime_flexible(inputs.date, inputs.end_time)

    if not start_dt or not end_dt:
        return "❌ Couldn't understand the provided date or time."

    if start_dt >= end_dt:
        return "❌ Start time must be before end time."

    event = {
        "summary": inputs.summary,
        "start": {"dateTime": start_dt.isoformat(), "timeZone": TIMEZONE},
        "end": {"dateTime": end_dt.isoformat(), "timeZone": TIMEZONE},
    }

    try:
        service.events().insert(calendarId=CALENDAR_ID, body=event).execute()
        return f"✅ Meeting booked on {inputs.date} from {inputs.start_time} to {inputs.end_time}."
    except Exception as e:
        return f"❌ Failed to book the meeting: {e}"

class CheckAvailabilityInput(BaseModel):
    date: str
    start_time: str
    end_time: str

def check_availability(inputs: CheckAvailabilityInput) -> str:
    start_dt = parse_datetime_flexible(inputs.date, inputs.start_time)
    end_dt = parse_datetime_flexible(inputs.date, inputs.end_time)
    if not start_dt or not end_dt:
        return "❌ Couldn't understand the time range."
    
    events = service.events().list(
        calendarId=CALENDAR_ID,
        timeMin=start_dt.isoformat(),
        timeMax=end_dt.isoformat(),
        singleEvents=True,
        orderBy="startTime"
    ).execute().get("items", [])

    return "✅ You are free." if not events else "🗓️ You have events during that time."

class CheckScheduleInput(BaseModel):
    date: str

def check_schedule(inputs: CheckScheduleInput) -> str:
    start_dt = dateparser.parse(
        f"{inputs.date} 00:00", settings={"TIMEZONE": TIMEZONE, "RETURN_AS_TIMEZONE_AWARE": True}
    )
    end_dt = dateparser.parse(
        f"{inputs.date} 23:59", settings={"TIMEZONE": TIMEZONE, "RETURN_AS_TIMEZONE_AWARE": True}
    )
    if not start_dt or not end_dt:
        return "❌ Couldn't parse the date."

    events = service.events().list(
        calendarId=CALENDAR_ID,
        timeMin=start_dt.isoformat(),
        timeMax=end_dt.isoformat(),
        singleEvents=True,
        orderBy="startTime"
    ).execute().get("items", [])

    if not events:
        return f"✅ No events scheduled for {inputs.date}."

    return "\n".join([
        f"{e['summary']} from {e['start']['dateTime']} to {e['end']['dateTime']}"
        for e in events
    ])

class FindFreeSlotsInput(BaseModel):
    date: str
    duration_minutes: Optional[int] = 60

def find_free_slots(inputs: FindFreeSlotsInput) -> str:
    start_dt = dateparser.parse(f"{inputs.date} 00:00", settings={"TIMEZONE": TIMEZONE, "RETURN_AS_TIMEZONE_AWARE": True})
    end_dt = dateparser.parse(f"{inputs.date} 23:59", settings={"TIMEZONE": TIMEZONE, "RETURN_AS_TIMEZONE_AWARE": True})
    if not start_dt or not end_dt:
        return "❌ Couldn't parse the date."

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
        if (start - current).total_seconds() >= inputs.duration_minutes * 60:
            free_slots.append(f"{current.strftime('%I:%M %p')} to {start.strftime('%I:%M %p')}")
        current = max(current, end)

    if (end_dt - current).total_seconds() >= inputs.duration_minutes * 60:
        free_slots.append(f"{current.strftime('%I:%M %p')} to {end_dt.strftime('%I:%M %p')}")

    return "\n".join(free_slots) if free_slots else "❌ No free slots found."


# This file now uses natural language parsing entirely without Pydantic.




