# --- googlecalendar.py ---
from google.oauth2 import service_account
from googleapiclient.discovery import build
import json, os
from datetime import datetime, timedelta
import pytz
import dateparser

creds_json = os.getenv("GOOGLE_CREDENTIALS_JSON")
info = json.loads(creds_json)
credentials = service_account.Credentials.from_service_account_info(
    info, scopes=["https://www.googleapis.com/auth/calendar"]
)
service = build("calendar", "v3", credentials=credentials)
CALENDAR_ID = "devyanisharmaa15@gmail.com"
TIMEZONE = "Asia/Kolkata"


def parse_date_time(date_str, start_time_str, end_time_str):
    try:
        start_dt = dateparser.parse(
            f"{date_str} {start_time_str}",
            settings={"TIMEZONE": TIMEZONE, "RETURN_AS_TIMEZONE_AWARE": True}
        )
        end_dt = dateparser.parse(
            f"{date_str} {end_time_str}",
            settings={"TIMEZONE": TIMEZONE, "RETURN_AS_TIMEZONE_AWARE": True}
        )
        return start_dt, end_dt
    except:
        return None, None


def book_event_natural(prompt: str) -> str:
    try:
        parts = prompt.lower().split("from")
        if len(parts) != 2:
            return "❌ Use format like 'Monday from 2 PM to 3 PM'."

        date_part = parts[0].strip()
        time_range = parts[1].split("to")
        if len(time_range) != 2:
            return "❌ Couldn't parse time range. Use '2 PM to 3 PM'."

        start_time = time_range[0].strip()
        end_time = time_range[1].strip()
        start_dt, end_dt = parse_date_time(date_part, start_time, end_time)

        if not start_dt or not end_dt:
            return f"❌ Couldn't parse date/time from input: {prompt}"

        if start_dt >= end_dt:
            return "❌ Start time must be before end time."

        body = {
            "summary": "Meeting",
            "start": {"dateTime": start_dt.isoformat(), "timeZone": TIMEZONE},
            "end": {"dateTime": end_dt.isoformat(), "timeZone": TIMEZONE},
        }
        service.events().insert(calendarId=CALENDAR_ID, body=body).execute()
        return f"✅ Meeting booked on {date_part} from {start_time} to {end_time}."
    except Exception as e:
        return f"❌ Failed to book meeting: {e}"


def check_availability_natural(prompt: str) -> str:
    try:
        parts = prompt.lower().split("from")
        if len(parts) != 2:
            return "❌ Use format like 'Monday from 2 PM to 3 PM'."

        date_part = parts[0].strip()
        time_range = parts[1].split("to")
        if len(time_range) != 2:
            return "❌ Couldn't parse time range. Use '2 PM to 3 PM'."

        start_time = time_range[0].strip()
        end_time = time_range[1].strip()
        start_dt, end_dt = parse_date_time(date_part, start_time, end_time)

        if not start_dt or not end_dt:
            return f"❌ Couldn't parse date/time from input: {prompt}"

        events = service.events().list(
            calendarId=CALENDAR_ID,
            timeMin=start_dt.isoformat(),
            timeMax=end_dt.isoformat(),
            singleEvents=True,
            orderBy="startTime"
        ).execute().get("items", [])

        return "✅ You are free during that time." if not events else "🗓️ You have events during that time."
    except Exception as e:
        return f"❌ Failed to check availability: {e}"


def check_schedule_day(prompt: str) -> str:
    try:
        start_dt = dateparser.parse(f"{prompt} 00:00", settings={"TIMEZONE": TIMEZONE, "RETURN_AS_TIMEZONE_AWARE": True})
        end_dt = dateparser.parse(f"{prompt} 23:59", settings={"TIMEZONE": TIMEZONE, "RETURN_AS_TIMEZONE_AWARE": True})

        if not start_dt or not end_dt:
            return f"❌ Couldn't parse the date: {prompt}"

        events = service.events().list(
            calendarId=CALENDAR_ID,
            timeMin=start_dt.isoformat(),
            timeMax=end_dt.isoformat(),
            singleEvents=True,
            orderBy="startTime"
        ).execute().get("items", [])

        if not events:
            return f"✅ No events scheduled for {prompt}."

        return "\n".join([
            f"{e['summary']} from {e['start']['dateTime']} to {e['end']['dateTime']}"
            for e in events
        ])
    except Exception as e:
        return f"❌ Failed to fetch schedule: {e}"


def find_free_slots(prompt: str) -> str:
    try:
        start_dt = dateparser.parse(f"{prompt} 00:00", settings={"TIMEZONE": TIMEZONE, "RETURN_AS_TIMEZONE_AWARE": True})
        end_dt = dateparser.parse(f"{prompt} 23:59", settings={"TIMEZONE": TIMEZONE, "RETURN_AS_TIMEZONE_AWARE": True})

        if not start_dt or not end_dt:
            return f"❌ Couldn't parse the date: {prompt}"

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
            if (start - current).total_seconds() >= 3600:
                free_slots.append(f"{current.strftime('%I:%M %p')} to {start.strftime('%I:%M %p')}")
            current = max(current, end)

        if (end_dt - current).total_seconds() >= 3600:
            free_slots.append(f"{current.strftime('%I:%M %p')} to {end_dt.strftime('%I:%M %p')}")

        return "\n".join(free_slots) if free_slots else f"❌ No free 1-hour slots found on {prompt}."
    except Exception as e:
        return f"❌ Failed to find slots: {e}"


# This file now uses natural language parsing entirely without Pydantic.




