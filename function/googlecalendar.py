import dateparser
from google.oauth2 import service_account
from googleapiclient.discovery import build
from datetime import datetime
import os
import json

# Load credentials securely from environment variable
creds_json = os.getenv("GOOGLE_CREDENTIALS_JSON")
if not creds_json:
    raise ValueError("❌ GOOGLE_CREDENTIALS_JSON environment variable not set!")

info = json.loads(creds_json)
credentials = service_account.Credentials.from_service_account_info(info)
service = build("calendar", "v3", credentials=credentials)
CALENDAR_ID = "devyanisharmaa15@gmail.com"


def book_event(summary, start_time, end_time):
    try:
        event = {
            "summary": summary,
            "start": {
                "dateTime": start_time,
                "timeZone": "Asia/Kolkata",
            },
            "end": {
                "dateTime": end_time,
                "timeZone": "Asia/Kolkata",
            },
        }
        event = service.events().insert(calendarId=CALENDAR_ID, body=event).execute()
        return f"✅ Event '{summary}' booked from {start_time} to {end_time}."
    except Exception as e:
        return f"❌ Booking failed: {str(e)}"


def book_event_natural(text):
    try:
        parts = text.lower().split(" to ")
        if len(parts) != 2:
            return "❌ Please provide time in format like: 4 PM to 5 PM today"
        start = dateparser.parse(parts[0])
        end = dateparser.parse(parts[1])
        if not start or not end:
            return "❌ Could not parse the start or end time."
        return book_event("Meeting", start.isoformat(), end.isoformat())
    except Exception as e:
        return f"❌ Error parsing times: {str(e)}"


def check_availability():
    try:
        now = datetime.utcnow().isoformat() + 'Z'
        events = service.events().list(
            calendarId=CALENDAR_ID,
            timeMin=now,
            maxResults=5,
            singleEvents=True,
            orderBy="startTime"
        ).execute()
        times = [event["start"]["dateTime"] for event in events.get("items", [])]
        return times or ["✅ No events found"]
    except Exception as e:
        return f"❌ Error checking availability: {str(e)}"

