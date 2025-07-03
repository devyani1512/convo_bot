from google.oauth2 import service_account
from googleapiclient.discovery import build
import json, os
from datetime import datetime, timedelta
import pytz
import dateparser

# Load credentials and initialize Google Calendar service
creds_json = os.getenv("GOOGLE_CREDENTIALS_JSON")
info = json.loads(creds_json)
credentials = service_account.Credentials.from_service_account_info(
    info, scopes=["https://www.googleapis.com/auth/calendar"]
)
service = build("calendar", "v3", credentials=credentials)
CALENDAR_ID = "primary"  # Use actual email if necessary

def parse_datetime(text):
    return dateparser.parse(
        text,
        settings={"TIMEZONE": "Asia/Kolkata", "RETURN_AS_TIMEZONE_AWARE": True},
    )

def book_event_natural(time_text: str) -> str:
    times = time_text.lower().split("to")
    if len(times) != 2:
        return "❌ Format error: Use 'from X to Y' format."

    start_time = parse_datetime(times[0].strip())
    end_time = parse_datetime(times[1].strip())
    if not start_time or not end_time:
        return "❌ Could not parse the time input."

    body = {
        "summary": "Meeting",
        "start": {"dateTime": start_time.isoformat(), "timeZone": "Asia/Kolkata"},
        "end": {"dateTime": end_time.isoformat(), "timeZone": "Asia/Kolkata"},
    }

    service.events().insert(calendarId=CALENDAR_ID, body=body).execute()
    return f"✅ Meeting booked from {times[0].strip()} to {times[1].strip()}."

def check_availability_natural(time_range: str) -> str:
    times = time_range.lower().split("to")
    if len(times) != 2:
        return "❌ Please provide a time range like '3 PM to 4 PM today'."

    start_time = parse_datetime(times[0].strip())
    end_time = parse_datetime(times[1].strip())
    if not start_time or not end_time:
        return "❌ Unable to parse the times. Please try again."

    events = service.events().list(
        calendarId=CALENDAR_ID,
        timeMin=start_time.isoformat(),
        timeMax=end_time.isoformat(),
        singleEvents=True,
        orderBy="startTime"
    ).execute().get("items", [])

    return "✅ You are free during that time." if not events else "❌ You have events during that time."

def check_schedule_day(day_text: str) -> str:
    day_start = parse_datetime(f"{day_text} 00:00")
    day_end = parse_datetime(f"{day_text} 23:59")
    if not day_start or not day_end:
        return "❌ Couldn't understand the day you're referring to."

    events = service.events().list(
        calendarId=CALENDAR_ID,
        timeMin=day_start.isoformat(),
        timeMax=day_end.isoformat(),
        singleEvents=True,
        orderBy="startTime"
    ).execute().get("items", [])

    if not events:
        return f"✅ You are completely free on {day_text}."

    return "\n".join([
        f"🗓️ {e['summary']} from {e['start']['dateTime']} to {e['end']['dateTime']}"
        for e in events
    ])

def find_free_slots(day: str, duration_minutes: int = 60) -> str:
    start_dt = parse_datetime(f"{day} 00:00")
    if not start_dt:
        return "❌ Unable to parse the requested day."

    end_dt = start_dt + timedelta(hours=23, minutes=59)

    events = service.events().list(
        calendarId=CALENDAR_ID,
        timeMin=start_dt.isoformat(),
        timeMax=end_dt.isoformat(),
        singleEvents=True,
        orderBy="startTime"
    ).execute().get("items", [])

    busy_times = [
        (parse_datetime(e["start"]["dateTime"]), parse_datetime(e["end"]["dateTime"]))
        for e in events
    ]
    busy_times.sort()

    current = start_dt
    free_slots = []

    for start, end in busy_times:
        if (start - current).total_seconds() >= duration_minutes * 60:
            free_slots.append(f"{current.strftime('%I:%M %p')} to {start.strftime('%I:%M %p')}")
        current = max(current, end)

    if (end_dt - current).total_seconds() >= duration_minutes * 60:
        free_slots.append(f"{current.strftime('%I:%M %p')} to {end_dt.strftime('%I:%M %p')}")

    return (
        "\n".join(free_slots)
        if free_slots
        else f"❌ No free {duration_minutes}-minute slots found on {day}."
    )


