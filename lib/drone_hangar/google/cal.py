from datetime import date, datetime
import json
import logging
import pickle
import os
import re

from google.oauth2 import service_account
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request

# try:
#     from ..utils import storage_path
# except:
#     from lib.drone_hangar.utils import storage_path

def storage_path(uri):
    path = 'lib/drone_hangar/static'
    check = ''
    p_list = path.split('/')

    p_len = len(p_list)

    while p_len != 0:
        check = '/'.join([p_list[p_len - 1], check])
        if os.path.exists(check):
            result = os.path.join(check, uri)
            print(
                ' '.join([
                    '>>> Storage file populated at', result
                    ])
            )
            return result

        p_len = p_len - 1

    return os.path.abspath(result)

def get_credentials():
    creds = None
    SCOPES = ['https://www.googleapis.com/auth/calendar.readonly']
    SERVICE_ACCOUNT_FILE = os.path.join(os.getcwd(), 'google/credentials/google-service-account.json')
    # The file token.pickle stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
    # if os.path.exists('gapi-token.pickle'):
    #     with open('gapi-token.pickle', 'rb') as token:
    #         creds = pickle.load(token)
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            creds = service_account.Credentials.from_service_account_file(
                SERVICE_ACCOUNT_FILE, scopes=SCOPES)
            # creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
        # with open('gapi-token.pickle', 'wb') as token:
        #     pickle.dump(creds, token)
    
    return creds

def get_events():
    service = build('calendar', 'v3', credentials=get_credentials())

    now = datetime.utcnow().isoformat() + 'Z' # 'Z' indicates UTC time
    # The Calendar API needs to be fed time in a very specific format.
    start = date(date.today().year, 1, 1).strftime('%Y-%m-%dT00:00:00-07:00')
    end = date(date.today().year, 12, 31).strftime('%Y-%m-%dT23:59:59-07:00')
    events = service.events()
    
    single_results = events.list(
        calendarId='i3srpdc24fn8lkska1il6ann20@group.calendar.google.com',
        timeMin=start,
        timeMax=end,
        maxResults=250, singleEvents=True,
        orderBy='startTime'
    ).execute()
    
    recurring_results = events.list(
        calendarId='i3srpdc24fn8lkska1il6ann20@group.calendar.google.com',
        timeMin=start,
        timeMax=end,
        maxResults=250, singleEvents=False
    ).execute()

    with open(storage_path('google/calendar.json'), 'w') as f:
        json.dump(single_results.get('items', []), f, indent=4, sort_keys=True, default=str)

    with open(storage_path('google/recurrence.json'), 'w') as f:
        json.dump(recurring_results.get('items', []), f, indent=4, sort_keys=True, default=str)

if __name__ == "__main__":
    get_events()
