# from google.oauth2 import service_account
# from googleapiclient.discovery import build
# import os, json
# from datetime import datetime, timedelta
# import pytz
# import dateparser

# # Setup credentials and calendar service
# creds_json = os.getenv("GOOGLE_CREDENTIALS_JSON")
# info = json.loads(creds_json)
# credentials = service_account.Credentials.from_service_account_info(
#     info, scopes=["https://www.googleapis.com/auth/calendar"]
# )
# service = build("calendar", "v3", credentials=credentials)

# CALENDAR_ID = "devyanisharmaa15@gmail.com"
# TIMEZONE = "Asia/Kolkata"

# # Utility: Parse date and time into datetime object
# def parse_date_time(date_str, time_str):
#     return dateparser.parse(
#         f"{date_str} {time_str}",
#         settings={"TIMEZONE": TIMEZONE, "RETURN_AS_TIMEZONE_AWARE": True}
#     )

# # ✅ Book an event
# def book_event(date: str, start_time: str, end_time: str, summary: str = "Meeting") -> str:
#     start_dt = parse_date_time(date, start_time)
#     end_dt = parse_date_time(date, end_time)

#     if not start_dt or not end_dt or start_dt >= end_dt:
#         return "❌ Invalid or unclear time range."

#     body = {
#         "summary": summary,
#         "start": {"dateTime": start_dt.isoformat(), "timeZone": TIMEZONE},
#         "end": {"dateTime": end_dt.isoformat(), "timeZone": TIMEZONE},
#     }

#     try:
#         service.events().insert(calendarId=CALENDAR_ID, body=body).execute()
#         return f"✅ Meeting booked on {date} from {start_time} to {end_time}."
#     except Exception as e:
#         return f"❌ Failed to book meeting: {e}"

# # ✅ Check availability
# def check_availability(date: str, start_time: str, end_time: str) -> str:
#     start_dt = parse_date_time(date, start_time)
#     end_dt = parse_date_time(date, end_time)

#     if not start_dt or not end_dt:
#         return "❌ Couldn't parse time range."

#     events = service.events().list(
#         calendarId=CALENDAR_ID,
#         timeMin=start_dt.isoformat(),
#         timeMax=end_dt.isoformat(),
#         singleEvents=True,
#         orderBy="startTime"
#     ).execute().get("items", [])

#     return "✅ You are free during that time." if not events else "🗓️ You have events during that time."

# # ✅ Check schedule for a full day
# def check_schedule(date: str) -> str:
#     start_dt = parse_date_time(date, "00:00")
#     end_dt = parse_date_time(date, "23:59")

#     if not start_dt or not end_dt:
#         return "❌ Couldn't parse date."

#     events = service.events().list(
#         calendarId=CALENDAR_ID,
#         timeMin=start_dt.isoformat(),
#         timeMax=end_dt.isoformat(),
#         singleEvents=True,
#         orderBy="startTime"
#     ).execute().get("items", [])

#     if not events:
#         return f"✅ No events scheduled for {date}."

#     return "\n".join([
#         f"{e['summary']} from {e['start']['dateTime']} to {e['end']['dateTime']}" for e in events
#     ])

# # ✅ Find free time slots
# def find_free_slots(date: str, duration_minutes: int = 60) -> str:
#     start_dt = parse_date_time(date, "00:00")
#     end_dt = parse_date_time(date, "23:59")

#     events = service.events().list(
#         calendarId=CALENDAR_ID,
#         timeMin=start_dt.isoformat(),
#         timeMax=end_dt.isoformat(),
#         singleEvents=True,
#         orderBy="startTime"
#     ).execute().get("items", [])

#     busy_times = [(dateparser.parse(e["start"]["dateTime"]), dateparser.parse(e["end"]["dateTime"])) for e in events]
#     busy_times.sort()

#     current = start_dt
#     free_slots = []

#     for start, end in busy_times:
#         if (start - current).total_seconds() >= duration_minutes * 60:
#             free_slots.append(f"{current.strftime('%I:%M %p')} to {start.strftime('%I:%M %p')}")
#         current = max(current, end)

#     if (end_dt - current).total_seconds() >= duration_minutes * 60:
#         free_slots.append(f"{current.strftime('%I:%M %p')} to {end_dt.strftime('%I:%M %p')}")

#     return "\n".join(free_slots) if free_slots else f"❌ No free {duration_minutes}-minute slots on {date}."


# if __name__ == "__main__":
#     result = book_event(
#         date="9th July",
#         start_time="4 PM",
#         end_time="5 PM",
#         summary="Test Meeting"
#     )
#     print(result)





# from google.oauth2 import service_account
# from googleapiclient.discovery import build
# import os, json
# from datetime import datetime, timedelta
# import pytz
# import dateparser

# # ---- Setup Google Calendar API ----
# creds_json = os.getenv("GOOGLE_CREDENTIALS_JSON")
# info = json.loads(creds_json)
# credentials = service_account.Credentials.from_service_account_info(
#     info, scopes=["https://www.googleapis.com/auth/calendar"]
# )
# service = build("calendar", "v3", credentials=credentials)

# CALENDAR_ID = "devyanisharmaa15@gmail.com"
# TIMEZONE = "Asia/Kolkata"

# # ---- Utilities ----
# def parse_date_time(date_str, time_str):
#     return dateparser.parse(
#         f"{date_str} {time_str}",
#         settings={"TIMEZONE": TIMEZONE, "RETURN_AS_TIMEZONE_AWARE": True}
#     )

# def parse_reminder_string(reminder_str: str) -> list[int]:
#     """
#     Parse strings like '1 hour and 15 minutes' → [60, 15]
#     """
#     if not reminder_str:
#         return [15]
#     reminder_str = reminder_str.lower()
#     reminders = []
#     if "hour" in reminder_str:
#         hours = reminder_str.split("hour")[0].strip()
#         if hours.isdigit():
#             reminders.append(int(hours) * 60)
#     if "minute" in reminder_str:
#         if "and" in reminder_str:
#             minutes = reminder_str.split("and")[-1]
#         else:
#             minutes = reminder_str.split("minute")[0]
#         minutes = "".join(filter(str.isdigit, minutes))
#         if minutes:
#             reminders.append(int(minutes))
#     if not reminders:
#         reminders = [15]
#     return reminders

# # ---- Book Event ----
# def book_event(
#     date: str,
#     start_time: str,
#     end_time: str,
#     summary: str = "Meeting",
#     reminder: str = None
# ) -> str:
#     start_dt = parse_date_time(date, start_time)
#     end_dt = parse_date_time(date, end_time)

#     if not start_dt or not end_dt or start_dt >= end_dt:
#         return "❌ Invalid or unclear time range."

#     reminder_minutes_list = parse_reminder_string(reminder)
#     overrides = [{"method": "popup", "minutes": m} for m in reminder_minutes_list]

#     body = {
#         "summary": summary,
#         "start": {"dateTime": start_dt.isoformat(), "timeZone": TIMEZONE},
#         "end": {"dateTime": end_dt.isoformat(), "timeZone": TIMEZONE},
#         "reminders": {
#             "useDefault": False,
#             "overrides": overrides
#         }
#     }

#     try:
#         service.events().insert(calendarId=CALENDAR_ID, body=body).execute()
#         mins = ", ".join([f"{m} min" for m in reminder_minutes_list])
#         return f"✅ Meeting booked on {date} from {start_time} to {end_time} with reminders {mins} before."
#     except Exception as e:
#         return f"❌ Failed to book meeting: {e}"

# # ---- Cancel Event by Summary + Date ----
# def cancel_event(summary: str, date: str) -> str:
#     start_dt = parse_date_time(date, "00:00")
#     end_dt = parse_date_time(date, "23:59")

#     if not start_dt or not end_dt:
#         return "❌ Couldn't parse date."

#     try:
#         events = service.events().list(
#             calendarId=CALENDAR_ID,
#             timeMin=start_dt.isoformat(),
#             timeMax=end_dt.isoformat(),
#             singleEvents=True,
#             orderBy="startTime"
#         ).execute().get("items", [])

#         for event in events:
#             if event.get("summary", "").lower() == summary.lower():
#                 service.events().delete(calendarId=CALENDAR_ID, eventId=event["id"]).execute()
#                 return f"🗑️ Cancelled event: '{summary}' on {date}."
#         return f"⚠️ No event titled '{summary}' found on {date}."
#     except Exception as e:
#         return f"❌ Failed to cancel event: {e}"

# # ---- Check Availability ----
# def check_availability(date: str, start_time: str, end_time: str) -> str:
#     start_dt = parse_date_time(date, start_time)
#     end_dt = parse_date_time(date, end_time)

#     if not start_dt or not end_dt:
#         return "❌ Couldn't parse time range."

#     events = service.events().list(
#         calendarId=CALENDAR_ID,
#         timeMin=start_dt.isoformat(),
#         timeMax=end_dt.isoformat(),
#         singleEvents=True,
#         orderBy="startTime"
#     ).execute().get("items", [])

#     return "✅ You are free during that time." if not events else "🗓️ You have events during that time."

# # ---- Check Day Schedule ----
# def check_schedule(date: str) -> str:
#     start_dt = parse_date_time(date, "00:00")
#     end_dt = parse_date_time(date, "23:59")

#     if not start_dt or not end_dt:
#         return "❌ Couldn't parse date."

#     events = service.events().list(
#         calendarId=CALENDAR_ID,
#         timeMin=start_dt.isoformat(),
#         timeMax=end_dt.isoformat(),
#         singleEvents=True,
#         orderBy="startTime"
#     ).execute().get("items", [])

#     if not events:
#         return f"✅ No events scheduled for {date}."

#     return "\n".join([
#         f"{e['summary']} from {e['start']['dateTime']} to {e['end']['dateTime']}" for e in events
#     ])

# # ---- Find Free Slots ----
# def find_free_slots(date: str, duration_minutes: int = 60) -> str:
#     start_dt = parse_date_time(date, "00:00")
#     end_dt = parse_date_time(date, "23:59")

#     events = service.events().list(
#         calendarId=CALENDAR_ID,
#         timeMin=start_dt.isoformat(),
#         timeMax=end_dt.isoformat(),
#         singleEvents=True,
#         orderBy="startTime"
#     ).execute().get("items", [])

#     busy_times = [(dateparser.parse(e["start"]["dateTime"]), dateparser.parse(e["end"]["dateTime"])) for e in events]
#     busy_times.sort()

#     current = start_dt
#     free_slots = []

#     for start, end in busy_times:
#         if (start - current).total_seconds() >= duration_minutes * 60:
#             free_slots.append(f"{current.strftime('%I:%M %p')} to {start.strftime('%I:%M %p')}")
#         current = max(current, end)

#     if (end_dt - current).total_seconds() >= duration_minutes * 60:
#         free_slots.append(f"{current.strftime('%I:%M %p')} to {end_dt.strftime('%I:%M %p')}")

#     return "\n".join(free_slots) if free_slots else f"❌ No free {duration_minutes}-minute slots on {date}."

import os, json, dateparser
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build
from datetime import datetime

TIMEZONE = "Asia/Kolkata"

def get_calendar_service():
    token_info = json.loads(os.getenv("CLIENT_CONFIG_JSON"))
    credentials = Credentials.from_authorized_user_info(info=token_info, scopes=["https://www.googleapis.com/auth/calendar"])
    return build("calendar", "v3", credentials=credentials)

def parse_date_time(date_str, time_str):
    return dateparser.parse(f"{date_str} {time_str}", settings={"TIMEZONE": TIMEZONE, "RETURN_AS_TIMEZONE_AWARE": True})

def parse_reminder_string(reminder_str):
    if not reminder_str:
        return [15]
    reminder_str = reminder_str.lower()
    reminders = []
    if "hour" in reminder_str:
        hours = reminder_str.split("hour")[0].strip()
        if hours.isdigit():
            reminders.append(int(hours) * 60)
    if "minute" in reminder_str:
        minutes = reminder_str.split("and")[-1] if "and" in reminder_str else reminder_str.split("minute")[0]
        minutes = "".join(filter(str.isdigit, minutes))
        if minutes:
            reminders.append(int(minutes))
    return reminders or [15]

def book_event(date, start_time, end_time, summary="Meeting", reminder=None):
    service = get_calendar_service()
    start_dt = parse_date_time(date, start_time)
    end_dt = parse_date_time(date, end_time)
    overrides = [{"method": "popup", "minutes": m} for m in parse_reminder_string(reminder)]
    body = {
        "summary": summary,
        "start": {"dateTime": start_dt.isoformat(), "timeZone": TIMEZONE},
        "end": {"dateTime": end_dt.isoformat(), "timeZone": TIMEZONE},
        "reminders": {"useDefault": False, "overrides": overrides}
    }
    try:
        service.events().insert(calendarId="primary", body=body).execute()
        return f"✅ Meeting booked on {date} from {start_time} to {end_time}."
    except Exception as e:
        return f"❌ Failed to book meeting: {e}"

def cancel_event(summary, date):
    service = get_calendar_service()
    start_dt = parse_date_time(date, "00:00")
    end_dt = parse_date_time(date, "23:59")
    try:
        events = service.events().list(calendarId="primary", timeMin=start_dt.isoformat(), timeMax=end_dt.isoformat(), singleEvents=True).execute().get("items", [])
        for event in events:
            if event.get("summary", "").lower() == summary.lower():
                service.events().delete(calendarId="primary", eventId=event["id"]).execute()
                return f"🗑️ Cancelled event: '{summary}' on {date}."
        return f"⚠️ No event titled '{summary}' found on {date}."
    except Exception as e:
        return f"❌ Failed to cancel event: {e}"

def check_availability(date, start_time, end_time):
    service = get_calendar_service()
    start_dt = parse_date_time(date, start_time)
    end_dt = parse_date_time(date, end_time)
    events = service.events().list(calendarId="primary", timeMin=start_dt.isoformat(), timeMax=end_dt.isoformat(), singleEvents=True).execute().get("items", [])
    return "✅ You are free during that time." if not events else "🗓️ You have events during that time."

def check_schedule(date):
    service = get_calendar_service()
    start_dt = parse_date_time(date, "00:00")
    end_dt = parse_date_time(date, "23:59")
    events = service.events().list(calendarId="primary", timeMin=start_dt.isoformat(), timeMax=end_dt.isoformat(), singleEvents=True).execute().get("items", [])
    if not events:
        return f"✅ No events scheduled for {date}."
    return "\n".join([f"{e['summary']} from {e['start']['dateTime']} to {e['end']['dateTime']}" for e in events])

def find_free_slots(date, duration_minutes=60):
    service = get_calendar_service()
    start_dt = parse_date_time(date, "00:00")
    end_dt = parse_date_time(date, "23:59")
    events = service.events().list(calendarId="primary", timeMin=start_dt.isoformat(), timeMax=end_dt.isoformat(), singleEvents=True).execute().get("items", [])
    busy = [(dateparser.parse(e["start"]["dateTime"]), dateparser.parse(e["end"]["dateTime"])) for e in events]
    busy.sort()
    current = start_dt
    free = []
    for start, end in busy:
        if (start - current).total_seconds() >= duration_minutes * 60:
            free.append(f"{current.strftime('%I:%M %p')} to {start.strftime('%I:%M %p')}")
        current = max(current, end)
    if (end_dt - current).total_seconds() >= duration_minutes * 60:
        free.append(f"{current.strftime('%I:%M %p')} to {end_dt.strftime('%I:%M %p')}")
    return "\n".join(free) if free else f"❌ No free {duration_minutes}-minute slots on {date}."
