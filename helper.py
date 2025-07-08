from datetime import datetime
from pathlib import Path
import json
import os
from google.oauth2.credentials import Credentials
from google.auth.transport.requests import Request
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build


SCOPES = ['https://www.googleapis.com/auth/calendar.readonly',"https://www.googleapis.com/auth/tasks.readonly" ]

def LoadInstructions(file_name):
    return json.loads(Path(f"{file_name}.json").read_text())

def today():
    return str(datetime.now().today().date())

def auth():
    creds = None
    if os.path.exists('token.json'):
        creds = Credentials.from_authorized_user_file('token.json', SCOPES)

    # if shortcut from token.json does not exist then make a shortcut. (don't need manual verfication with this)
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'client_secret.json', SCOPES)
            creds = flow.run_local_server(port=0)  # Opens browser window

        # Save token to avoid repeat logins
        with open('token.json', 'w') as token:
            token.write(creds.to_json())
    return creds

def tasks(creds):
    service = build('tasks','v1',credentials=creds)
    results = service.tasks().list(tasklist='@default').execute()
    tasks = results.get('items', [])
    today = []
    for task in tasks:
        due_date = datetime.strptime(task['due'], "%Y-%m-%dT%H:%M:%S.%fZ").date()
        if datetime.today().date() == due_date:
            today.append(task['title'])
    return today

def calender(creds,calendarId="primary",maxResults=10,singleEvents=True,orderBy='startTime'):
    service = build('calendar','v3',credentials=creds)
    
    now = datetime.utcnow().isoformat()+'Z'
    events_result = service.events().list(
        calendarId = calendarId,
        timeMin=now,
        maxResults=maxResults,
        singleEvents=singleEvents,
        orderBy=orderBy
    ).execute()

    events = events_result.get('items', [])
    today = []
    for event in events:
        print(event['start'])
        if event['start']==datetime.today().date():
            
            today.append({event['start']['date'],event['summary']})
        else:
            pass
    return today