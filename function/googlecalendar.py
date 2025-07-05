from google.oauth2 import service_account
from googleapiclient.discovery import build
import json, os
from datetime import datetime, timedelta
import pytz
import dateparser

# --- Google Auth Setup ---
creds_json = os.getenv("GOOGLE_CREDENTIALS_JSON")
info = json.loads(creds_json)
credentials = service_account.Credentials.from_service_account_info(
    info, scopes=["https://www.googleapis.com/auth/calendar"]
)
service = build("calendar", "v3", credentials=credentials)
CALENDAR_ID = "devyanisharmaa15@gmail.com"
TIMEZONE = "Asia/Kolkata"

# --- Date Parsing ---
def parse_date_time(date_str, time_str):
    try:
        dt = dateparser.parse(
            f"{date_str} {time_str}",
            settings={"TIMEZONE": TIMEZONE, "RETURN_AS_TIMEZONE_AWARE": True}
        )
        return dt
    except Exception as e:
        print(f"[Parse Error] {date_str} {time_str} -> {e}")
        return None

# --- Tool 1: Book Meeting ---
def book_event(date: str, start_time: str, end_time: str, summary: str = "Meeting") -> str:
    start_dt = parse_date_time(date, start_time)
    end_dt = parse_date_time(date, end_time)

    if not start_dt or not end_dt:
        return f"❌ Couldn't parse the date/time: {date}, {start_time} to {end_time}"

    if start_dt >= end_dt:
        return "❌ Invalid time range: Start time must be before end time."

    body = {
        "summary": summary,
        "start": {"dateTime": start_dt.isoformat(), "timeZone": TIMEZONE},
        "end": {"dateTime": end_dt.isoformat(), "timeZone": TIMEZONE},
    }

    try:
        service.events().insert(calendarId=CALENDAR_ID, body=body).execute()
        return f"✅ Meeting booked on {date} from {start_time} to {end_time}."
    except Exception as e:
        return f"❌ Failed to book meeting: {e}"

# --- Tool 2: Check Availability ---
def check_availability(date: str, start_time: str, end_time: str) -> str:
    start_dt = parse_date_time(date, start_time)
    end_dt = parse_date_time(date, end_time)

    if not start_dt or not end_dt:
        return f"❌ Couldn't parse the time range: {start_time} to {end_time} on {date}"

    events = service.events().list(
        calendarId=CALENDAR_ID,
        timeMin=start_dt.isoformat(),
        timeMax=end_dt.isoformat(),
        singleEvents=True,
        orderBy="startTime"
    ).execute().get("items", [])

    return "✅ You are free during that time." if not events else "🗓️ You have events during that time."

# --- Tool 3: Get Schedule for a Day ---
def check_schedule(date: str) -> str:
    start_dt = parse_date_time(date, "00:00")
    end_dt = parse_date_time(date, "23:59")

    if not start_dt or not end_dt:
        return f"❌ Couldn't parse the date: {date}."

    events = service.events().list(
        calendarId=CALENDAR_ID,
        timeMin=start_dt.isoformat(),
        timeMax=end_dt.isoformat(),
        singleEvents=True,
        orderBy="startTime"
    ).execute().get("items", [])

    if not events:
        return f"✅ No events scheduled for {date}."

    return "\n".join([
        f"{e['summary']} from {e['start']['dateTime']} to {e['end']['dateTime']}"
        for e in events
    ])

# --- Tool 4: Find Free Slots ---
def find_free_slots(date: str, duration_minutes: int = 60) -> str:
    start_dt = parse_date_time(date, "00:00")
    end_dt = parse_date_time(date, "23:59")

    if not start_dt or not end_dt:
        return f"❌ Couldn't parse the date: {date}."

    events = service.events().list(
        calendarId=CALENDAR_ID,
        timeMin=start_dt.isoformat(),
        timeMax=end_dt.isoformat(),
        singleEvents=True,
        orderBy="startTime"
    ).execute().get("items", [])

    busy = [(parse_date_time("", e["start"]["dateTime"]), parse_date_time("", e["end"]["dateTime"])) for e in events]
    busy.sort()

    free_slots = []
    current = start_dt

    for start, end in busy:
        if (start - current).total_seconds() >= duration_minutes * 60:
            free_slots.append(f"{current.strftime('%I:%M %p')} to {start.strftime('%I:%M %p')}")
        current = max(current, end)

    if (end_dt - current).total_seconds() >= duration_minutes * 60:
        free_slots.append(f"{current.strftime('%I:%M %p')} to {end_dt.strftime('%I:%M %p')}")

    return "\n".join(free_slots) if free_slots else f"❌ No free {duration_minutes}-minute slots on {date}."

# This file now uses natural language parsing entirely without Pydantic.




