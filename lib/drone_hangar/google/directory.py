from datetime import date, datetime
import json
import logging
import pickle
import os
import re

from django.template.defaultfilters import slugify

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
    SCOPES = ['https://www.googleapis.com/auth/spreadsheets.readonly']
    SERVICE_ACCOUNT_FILE = os.path.join(os.getcwd(), 'secrets/google-service-account.json')
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

def get_directory():
    '''
    Returns a dict with the keys being the slugified text of the first column.
    '''
    ssid = '1S9iTiyFCdUzU8khkKiYPDWn3RWNgp-AKWuzxq9PWNP4'
    service = build('sheets', 'v4', credentials=get_credentials(),
        cache_discovery=False)

    sheet = service.spreadsheets().values().get(spreadsheetId=ssid, range="Directory!A1:ZZ").execute()

    # Django's slugify() returns SafeText. We coerce them back to strings so that the output is plain and easy to work with.
    fields = [ str(slugify(v)) for v in sheet['values'][0] ]
    data = { str(slugify(v[0])): dict(zip(fields, v)) for v in sheet['values'][1:] }

    return data

if __name__ == "__main__":
    get_directory()
