import os

from django.urls import reverse

import dropbox
from dropbox import DropboxOAuth2Flow

'''
This example walks through a basic oauth flow using the existing long-lived token type
Populate your app key and app secret in order to run this locally
'''
APP_KEY = os.environ["DROPBOX_APP_KEY"]
APP_SECRET = os.environ["DROPBOX_APP_SECRET"]

# TODO: Eventually, the app will need to authorize using the standard flow. For right now, I have one permanent access token in my environment variables, which is secure until it gets leaked.

# auth_flow = DropboxOAuth2Flow(APP_KEY, reverse('dropbox.home'))

# authorize_url = auth_flow.start()
# print("1. Go to: " + authorize_url)
# print("2. Click \"Allow\" (you might have to log in first).")
# print("3. Copy the authorization code.")
# auth_code = input("Enter the authorization code here: ").strip()

# try:
#     oauth_result = auth_flow.finish(auth_code)
# except Exception as e:
#     print('Error: %s' % (e,))
#     exit(1)

# with dropbox.Dropbox(oauth2_access_token=oauth_result.access_token) as dbx:
#     dbx.users_get_current_account()
#     print("Successfully set up client!")
