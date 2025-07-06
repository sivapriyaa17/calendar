import datetime
from google.oauth2 import service_account
from googleapiclient.discovery import build

SCOPES = ['https://www.googleapis.com/auth/calendar']
SERVICE_ACCOUNT_FILE = "backend/credentials/service_account.json"
CALENDAR_ID = 'primary'  

credentials = service_account.Credentials.from_service_account_file(
    SERVICE_ACCOUNT_FILE, scopes=SCOPES)
service = build('calendar', 'v3', credentials=credentials)

def free_slots(date_str):
    start = datetime.datetime.fromisoformat(date_str)
    end = start + datetime.timedelta(days=1)
    body = {
        "timeMin": start.isoformat() + 'Z',
        "timeMax": end.isoformat() + 'Z',
        "timeZone": "Asia/Kolkata",
        "items": [{"id": CALENDAR_ID}]
    }
    response = service.freebusy().query(body=body).execute()
    busy_times = response['calendars'][CALENDAR_ID]['busy']
    return "Busy slots: " + str(busy_times)

def book_event(date, time, summary):
    start_dt = datetime.datetime.fromisoformat(f"{date}T{time}")
    end_dt = start_dt + datetime.timedelta(minutes=30)
    event = {
        'summary': summary,
        'start': {'dateTime': start_dt.isoformat(), 'timeZone': 'Asia/Kolkata'},
        'end': {'dateTime': end_dt.isoformat(), 'timeZone': 'Asia/Kolkata'},
    }
    service.events().insert(calendarId=CALENDAR_ID, body=event).execute()
    return f"✅ Booking confirmed on {date} at {time} for '{summary}'"
