from google.oauth2 import service_account
from googleapiclient.discovery import build
import json, os, re
from datetime import datetime, timedelta
import pytz
import dateparser

# Load service account credentials
creds_json = os.getenv("GOOGLE_CREDENTIALS_JSON")
info = json.loads(creds_json)
credentials = service_account.Credentials.from_service_account_info(
    info, scopes=["https://www.googleapis.com/auth/calendar"]
)

# Build calendar service
service = build("calendar", "v3", credentials=credentials)
CALENDAR_ID = "devyanisharmaa15@gmail.com"  # Replace with your calendar ID

# Helper: Convert weekday name to datetime
def get_next_weekday(weekday_name):
    weekday_name = weekday_name.lower()
    today = datetime.now(pytz.timezone("Asia/Kolkata"))
    weekdays = ['monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'sunday']
    if weekday_name not in weekdays:
        return None
    target = weekdays.index(weekday_name)
    days_ahead = (target - today.weekday() + 7) % 7
    days_ahead = 7 if days_ahead == 0 else days_ahead
    return today + timedelta(days=days_ahead)

# Helper: Parse general datetime with dateparser
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

# 🔍 Natural language date+time extractor
def parse_input_naturally(text: str):
    # Extract times like "3 PM", "10:30 AM"
    times = re.findall(r'(\d{1,2}(?::\d{2})?\s*(AM|PM))', text, re.IGNORECASE)
    time_strs = [f"{t[0]} {t[1]}" for t in times]

    # Check for full dates like "9th July", "15 August"
    date_match = re.search(r'\d{1,2}(st|nd|rd|th)?\s+\w+', text, re.IGNORECASE)
    date_str = date_match.group(0) if date_match else None

    # Check for relative days like "Monday", "tomorrow", etc.
    weekday_match = re.search(r'\b(today|tomorrow|monday|tuesday|wednesday|thursday|friday|saturday|sunday)\b', text, re.IGNORECASE)
    day_str = weekday_match.group(0).lower() if weekday_match else None

    if not date_str and day_str:
        if day_str == "today":
            date_str = datetime.now(pytz.timezone("Asia/Kolkata")).strftime("%d %B %Y")
        elif day_str == "tomorrow":
            tomorrow = datetime.now(pytz.timezone("Asia/Kolkata")) + timedelta(days=1)
            date_str = tomorrow.strftime("%d %B %Y")
        else:
            dt = get_next_weekday(day_str)
            date_str = dt.strftime("%d %B %Y") if dt else None

    if len(time_strs) >= 2 and date_str:
        start_dt = parse_datetime(f"{date_str} {time_strs[0]}")
        end_dt = parse_datetime(f"{date_str} {time_strs[1]}")
        return start_dt, end_dt

    return None, None

# ✅ Book an event from natural input
def book_event_natural(time_text: str) -> str:
    try:
        if "to" not in time_text:
            return "⚠️ Format error: Please use 'from X to Y' format like '3 PM to 4 PM on 9th July'."

        parts = time_text.lower().split("to")
        start_raw = parts[0].strip()
        end_raw = parts[1].strip()

        # Use dateparser to extract datetime values
        start_time = parse_datetime(start_raw)
        end_time = parse_datetime(end_raw)

        # If only one has the date, apply to both
        if not start_time or not end_time:
            # Try to extract date from one side
            for phrase in ["on", "at"]:
                if phrase in start_raw:
                    base_date = start_raw.split(phrase)[-1].strip()
                    if not end_time:
                        end_time = parse_datetime(f"{end_raw} {base_date}")
                    if not start_time:
                        start_time = parse_datetime(f"{start_raw}")
                    break

        if not start_time or not end_time:
            return f"❌ Couldn't understand your time/date. Try: 'Book a meeting on 9th July from 3 PM to 4 PM'."

        if start_time >= end_time:
            return "⚠️ Invalid range: Start time must be before end time."

        body = {
            "summary": "Meeting",
            "start": {"dateTime": start_time.isoformat(), "timeZone": "Asia/Kolkata"},
            "end": {"dateTime": end_time.isoformat(), "timeZone": "Asia/Kolkata"},
        }

        service.events().insert(calendarId=CALENDAR_ID, body=body).execute()
        return f"✅ Meeting booked from {start_time.strftime('%I:%M %p, %d %b')} to {end_time.strftime('%I:%M %p, %d %b')}."

    except Exception as e:
        return f"❌ Booking failed due to error: {str(e)}"


# ✅ Check availability in a natural time range
def check_availability_natural(time_range: str) -> str:
    start_dt, end_dt = parse_input_naturally(time_range)

    if not start_dt or not end_dt:
        return f"❌ Couldn't parse time range: '{time_range}'"

    events = service.events().list(
        calendarId=CALENDAR_ID,
        timeMin=start_dt.isoformat(),
        timeMax=end_dt.isoformat(),
        singleEvents=True,
        orderBy="startTime"
    ).execute().get("items", [])

    return "✅ You're free during that time." if not events else "📅 You have events during that time."

# ✅ Check schedule for a given day
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
        return f"✅ No events scheduled for {day_text}."

    return "\n".join([
        f"{e['summary']} from {parse_datetime(e['start']['dateTime']).strftime('%I:%M %p')} to {parse_datetime(e['end']['dateTime']).strftime('%I:%M %p')}"
        for e in events
    ])

# ✅ Find free time slots
def find_free_slots(day: str, duration_minutes: int = 60) -> str:
    start_dt = parse_datetime(f"{day} 00:00")
    end_dt = parse_datetime(f"{day} 23:59")

    if not start_dt or not end_dt:
        return "❌ Couldn't parse the day input."

    events = service.events().list(
        calendarId=CALENDAR_ID,
        timeMin=start_dt.isoformat(),
        timeMax=end_dt.isoformat(),
        singleEvents=True,
        orderBy="startTime"
    ).execute().get("items", [])

    busy_times = [
        (parse_datetime(e["start"]["dateTime"]), parse_datetime(e["end"]["dateTime"]))
        for e in events if e.get("start") and e.get("end")
    ]
    busy_times.sort()

    current = start_dt
    free_slots = []

    for start, end in busy_times:
        if not start or not end:
            continue
        if (start - current).total_seconds() >= duration_minutes * 60:
            free_slots.append(f"{current.strftime('%I:%M %p')} to {start.strftime('%I:%M %p')}")
        current = max(current, end)

    if (end_dt - current).total_seconds() >= duration_minutes * 60:
        free_slots.append(f"{current.strftime('%I:%M %p')} to {end_dt.strftime('%I:%M %p')}")

    return "\n".join(free_slots) if free_slots else f"❌ No free {duration_minutes}-minute slots found on {day}."

