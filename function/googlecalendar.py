from google.oauth2 import service_account
from googleapiclient.discovery import build
import json, os
from datetime import timedelta
import pytz
import dateparser
from dateparser.search import search_dates

creds_json = os.getenv("GOOGLE_CREDENTIALS_JSON")
info = json.loads(creds_json)
credentials = service_account.Credentials.from_service_account_info(
    info, scopes=["https://www.googleapis.com/auth/calendar"]
)
service = build("calendar", "v3", credentials=credentials)
CALENDAR_ID = "devyanisharmaa15@gmail.com"  # your calendar

def parse_datetime(text):
    try:
        dt = dateparser.parse(
            text,
            settings={"TIMEZONE": "Asia/Kolkata", "RETURN_AS_TIMEZONE_AWARE": True}
        )
        return dt if dt else None
    except Exception as e:
        print(f"[DateParse Error] {text} → {e}")
        return None

def check_availability_natural(time_range: str) -> str:
    times = search_dates(
        time_range,
        settings={"TIMEZONE": "Asia/Kolkata", "RETURN_AS_TIMEZONE_AWARE": True}
    )
    if not times or len(times) < 2:
        return "❌ Please provide a valid time range like '3 PM to 4 PM today'."

    _, start_time = times[0]
    _, end_time = times[1]

    events = service.events().list(
        calendarId=CALENDAR_ID,
        timeMin=start_time.isoformat(),
        timeMax=end_time.isoformat(),
        singleEvents=True,
        orderBy="startTime"
    ).execute().get("items", [])

    return "✅ You are free during that time." if not events else "❌ You have events during that time."

def book_event_natural(text: str) -> str:
    results = search_dates(
        text,
        settings={"TIMEZONE": "Asia/Kolkata", "RETURN_AS_TIMEZONE_AWARE": True}
    )

    if not results or len(results) < 2:
        return "❌ Could not find two time values. Try something like 'Book from 2 PM to 3 PM on Friday'."

    _, start_dt = results[0]
    _, end_dt = results[1]

    if start_dt >= end_dt:
        return "❌ Start time must be before end time."

    body = {
        "summary": "Meeting",
        "start": {"dateTime": start_dt.isoformat(), "timeZone": "Asia/Kolkata"},
        "end": {"dateTime": end_dt.isoformat(), "timeZone": "Asia/Kolkata"},
    }

    try:
        service.events().insert(calendarId=CALENDAR_ID, body=body).execute()
        return f"✅ Meeting booked from {start_dt.strftime('%I:%M %p %d %b')} to {end_dt.strftime('%I:%M %p %d %b')}."
    except Exception as e:
        return f"❌ Failed to book meeting: {e}"

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
        return f"📅 No events scheduled for {day_text}."

    return "\n".join([
        f"📌 {e['summary']} from {e['start']['dateTime']} to {e['end']['dateTime']}"
        for e in events
    ])

def find_free_slots(day: str, duration_minutes: int = 60) -> str:
    start_dt = parse_datetime(f"{day} 00:00")
    end_dt = parse_datetime(f"{day} 23:59")

    if not start_dt or not end_dt:
        return "❌ Could not parse the day input."

    events = service.events().list(
        calendarId=CALENDAR_ID,
        timeMin=start_dt.isoformat(),
        timeMax=end_dt.isoformat(),
        singleEvents=True,
        orderBy="startTime"
    ).execute().get("items", [])

    busy_times = [(parse_datetime(e["start"]["dateTime"]), parse_datetime(e["end"]["dateTime"])) for e in events]
    busy_times.sort()

    current = start_dt
    free_slots = []

    for start, end in busy_times:
        if not start or not end:
            continue
        if (start - current).total_seconds() >= duration_minutes * 60:
            free_slots.append(f"🟢 {current.strftime('%I:%M %p')} to {start.strftime('%I:%M %p')}")
        current = max(current, end)

    if (end_dt - current).total_seconds() >= duration_minutes * 60:
        free_slots.append(f"🟢 {current.strftime('%I:%M %p')} to {end_dt.strftime('%I:%M %p')}")

    return "\n".join(free_slots) if free_slots else f"❌ No free {duration_minutes}-minute slots found on {day}."
