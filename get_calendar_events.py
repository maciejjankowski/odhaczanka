from datetime import datetime, timedelta
from google.oauth2 import service_account
from googleapiclient.discovery import build
import json

# Setup the credentials
SCOPES = ['https://www.googleapis.com/auth/calendar.readonly']
SERVICE_ACCOUNT_FILE = 'path/to/your/service-account-file.json'

credentials = service_account.Credentials.from_service_account_file(
        SERVICE_ACCOUNT_FILE, scopes=SCOPES)

# Build the service
service = build('calendar', 'v3', credentials=credentials)

# Call the Calendar API
now = datetime.utcnow().isoformat() + 'Z'  # 'Z' indicates UTC time
end_of_day = (datetime.utcnow() + timedelta(days=1)).isoformat() + 'Z'

events_result = service.events().list(calendarId='primary', timeMin=now,
                                      timeMax=end_of_day, singleEvents=True,
                                      orderBy='startTime').execute()
events = events_result.get('items', [])

# Display the events
events_data = []
for event in events:
    start = event['start'].get('dateTime', event['start'].get('date'))
    end = event['end'].get('dateTime', event['end'].get('date'))
    duration = datetime.fromisoformat(end) - datetime.fromisoformat(start)
    events_data.append({
        'title': event['summary'],
        'start_time': start,
        'end_time': end,
        'duration': str(duration)
    })

print(json.dumps(events_data, indent=2))
