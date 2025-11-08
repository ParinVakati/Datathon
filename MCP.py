# from google.oauth2.credentials import Credentials
# from google_auth_oauthlib.flow import InstalledAppFlow
# from google.auth.transport.requests import Request
# from googleapiclient.discovery import build
# import datetime
# import os.path
# import pickle

# class CalendarManager:
#     def __init__(self):
#         self.SCOPES = ['https://www.googleapis.com/auth/calendar.readonly']
#         self.creds = None
#         self.service = None

#     def authenticate(self):
#         """Authenticate with Google Calendar API."""
#         # Check if token.pickle exists with stored credentials
#         if os.path.exists('token.pickle'):
#             with open('token.pickle', 'rb') as token:
#                 self.creds = pickle.load(token)

#         # If no valid credentials available, let the user log in
#         if not self.creds or not self.creds.valid:
#             if self.creds and self.creds.expired and self.creds.refresh_token:
#                 self.creds.refresh(Request())
#             else:
#                 flow = InstalledAppFlow.from_client_secrets_file(
#                     'credentials.json', self.SCOPES)
#                 self.creds = flow.run_local_server(port=0)
            
#             # Save the credentials for the next run
#             with open('token.pickle', 'wb') as token:
#                 pickle.dump(self.creds, token)

#         self.service = build('calendar', 'v3', credentials=self.creds)

#     def get_upcoming_events(self, max_results=10):
#         """Get upcoming calendar events."""
#         if not self.service:
#             self.authenticate()

#         now = datetime.datetime.utcnow().isoformat() + 'Z'
#         events_result = self.service.events().list(
#             calendarId='primary',
#             timeMin=now,
#             maxResults=max_results,
#             singleEvents=True,
#             orderBy='startTime'
#         ).execute()
        
#         return events_result.get('items', [])

#     def check_availability(self, start_time, end_time):
#         """Check if user is free during a specific time period."""
#         if not self.service:
#             self.authenticate()

#         events_result = self.service.events().list(
#             calendarId='primary',
#             timeMin=start_time.isoformat() + 'Z',
#             timeMax=end_time.isoformat() + 'Z',
#             singleEvents=True,
#             orderBy='startTime'
#         ).execute()

#         events = events_result.get('items', [])
#         return len(events) == 0

#     def format_event_info(self, event):
#         """Format event information for display."""
#         start = event['start'].get('dateTime', event['start'].get('date'))
#         end = event['end'].get('dateTime', event['end'].get('date'))
#         return {
#             'summary': event.get('summary', 'No title'),
#             'start': start,
#             'end': end,
#             'location': event.get('location', 'No location specified')
#         }

# def main():
#     calendar_manager = CalendarManager()
    
#     # Get upcoming events
#     print("Fetching your upcoming events...")
#     events = calendar_manager.get_upcoming_events()

#     if not events:
#         print('No upcoming events found.')
#     else:
#         print('Upcoming events:')
#         for event in events:
#             event_info = calendar_manager.format_event_info(event)
#             print(f"\nEvent: {event_info['summary']}")
#             print(f"Start: {event_info['start']}")
#             print(f"End: {event_info['end']}")
#             print(f"Location: {event_info['location']}")

#     # Check availability for a specific time
#     now = datetime.datetime.utcnow()
#     test_start = now + datetime.timedelta(hours=1)
#     test_end = test_start + datetime.timedelta(hours=1)
    
#     is_available = calendar_manager.check_availability(test_start, test_end)
#     print(f"\nAvailability check for {test_start} to {test_end}:")
#     print("Available" if is_available else "Busy")

# if __name__ == '__main__':
#     main()

