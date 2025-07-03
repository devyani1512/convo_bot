from google.oauth2 import service_account
from googleapiclient.discovery import build
import json, os
from datetime import datetime, timedelta
import pytz
import dateparser

creds_json = os.getenv("GOOGLE_CREDENTIALS_JSON")
info = json.loads(creds_json)
credentials = service_account.Credentials.from_service_account_info(info, scopes=["https://www.googleapis.com/auth/calendar"])
service = build("calendar", "v3", credentials=credentials)
CALENDAR_ID = "primary"  # or your actual calendar ID if needed

def parse_datetime(text):
    dt = dateparser.parse(text, settings={"TIMEZONE": "Asia/Kolkata", "RETURN_AS_TIMEZONE_AWARE": True})
    return dt.isoformat() if dt else None
    def find_free_slots(day: str, duration_minutes: int = 60) -> str:
    from datetime import timedelta

    # Parse day start and end
    start_dt = dateparser.parse(f"{day} 00:00", settings={"TIMEZONE": "Asia/Kolkata", "RETURN_AS_TIMEZONE_AWARE": True})
    end_dt = start_dt + timedelta(hours=23, minutes=59)

    events = service.events().list(
        calendarId=CALENDAR_ID,
        timeMin=start_dt.isoformat(),
        timeMax=end_dt.isoformat(),
        singleEvents=True,
        orderBy="startTime"
    ).execute().get("items", [])

    # Create timeline
    busy_times = [(dateparser.parse(e["start"]["dateTime"]), dateparser.parse(e["end"]["dateTime"])) for e in events]

    # Sort
    busy_times.sort()

    # Walk through the day and find gaps
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
        timeMin=start_time,
        timeMax=end_time,
        singleEvents=True,
        orderBy="startTime"
    ).execute().get("items", [])

    return "✅ You are free during that time." if not events else "❌ You have events during that time."

def check_schedule_day(day_text: str) -> str:
    day_start = dateparser.parse(f"{day_text} 00:00", settings={"TIMEZONE": "Asia/Kolkata", "RETURN_AS_TIMEZONE_AWARE": True})
    day_end = dateparser.parse(f"{day_text} 23:59", settings={"TIMEZONE": "Asia/Kolkata", "RETURN_AS_TIMEZONE_AWARE": True})

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
        return f"📅 No events scheduled for {day_text}."
    return "\n".join([f"{e['summary']} from {e['start']['dateTime']} to {e['end']['dateTime']}" for e in events])

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
        "start": {"dateTime": start_time, "timeZone": "Asia/Kolkata"},
        "end": {"dateTime": end_time, "timeZone": "Asia/Kolkata"},
    }

    service.events().insert(calendarId=CALENDAR_ID, body=body).execute()
    return f"✅ Meeting booked from {times[0].strip()} to {times[1].strip()}."


