import dateparser
from google.oauth2 import service_account
from googleapiclient.discovery import build
from datetime import datetime
import json
import os


SCOPES = ['https://www.googleapis.com/auth/calendar']

CALENDAR_ID = 'primary'
service_account_info = json.loads(os.getenv("GOOGLE_SERVICE_ACCOUNT_JSON"))
credentials = service_account.Credentials.from_service_account_info(
    service_account_info, scopes=SCOPES)
service = build('calendar', 'v3', credentials=credentials)


def book_event_natural(text):
    """
    Book an event based on natural language input like:
    "today from 2 PM to 3 PM" or "tomorrow 10 AM to 11 AM"
    """
    try:
        parts = text.lower().split(" to ")
        if len(parts) != 2:
            return "❌ Please provide time like: today from 4 PM to 5 PM"

        start_raw, end_raw = parts
        start = dateparser.parse(start_raw)
        end = dateparser.parse(end_raw)

        if not start or not end:
            return "❌ Could not parse one or both time inputs."

        start_iso = start.isoformat()
        end_iso = end.isoformat()

        return book_event("Meeting", start_iso, end_iso)

    except Exception as e:
        return f"❌ Error parsing times: {str(e)}"

# ------------------- Book Event (ISO Format) --------------------

def book_event(summary, start_time, end_time):
    """
    Book an event using ISO 8601 datetime strings.
    """
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

# ------------------- Check Availability --------------------

def check_availability():
    """
    Check next 5 upcoming events.
    """
    try:
        now = datetime.utcnow().isoformat() + 'Z'
        events = service.events().list(
            calendarId=CALENDAR_ID,
            timeMin=now,
            maxResults=5,
            singleEvents=True,
            orderBy='startTime'
        ).execute()

        items = events.get('items', [])
        if not items:
            return "✅ No upcoming events."
        
        result = "📅 Upcoming events:\n"
        for event in items:
            start = event['start'].get('dateTime', event['start'].get('date'))
            summary = event.get('summary', 'No Title')
            result += f"- {summary}: {start}\n"
        return result

    except Exception as e:
        return f"❌ Failed to fetch availability: {str(e)}"
