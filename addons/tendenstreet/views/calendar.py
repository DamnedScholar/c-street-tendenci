from collections import defaultdict
from datetime import date, datetime
import json
import logging
import pickle
import os.path
import re

from django.views.generic.base import TemplateView
from django.views.generic.dates import YearMixin, MonthMixin, WeekMixin, DayMixin, DateMixin

# Some of these methods are similar to operations in django.contrib.humanize, but the Django module is all filters and we need to run these operations in the business logic. This package also has greater capabilities than what's in the framework.
import humanize

from google.oauth2 import service_account
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request

def get_credentials():
    creds = None
    SCOPES = ['https://www.googleapis.com/auth/calendar.readonly']
    SERVICE_ACCOUNT_FILE = 'addons/tendenstreet/credentials/google-service-account.json'
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
        # Save the credentials for the next run
        # with open('gapi-token.pickle', 'wb') as token:
        #     pickle.dump(creds, token)
    
    return creds

class Event:
    etag = ''
    id = ''
    summary = ''
    location = ''
    calendar_link = ''
    social_link = ''
    created = ''
    updated = ''
    description = ''
    creator = {}
    organizer = {}
    start = {}
    end = {}
    recurring_event_id = ''
    original_start_time = {}
    visibility = 'public'
    ical_uid = ''

    def __init__(self, event):
        if event.get('description'):
            desc = self.get_social_link(event)  # Return a tuple of (description, social_link)
            self.social_link = desc[1]          # Link to social media
            self.description = desc[0]          # HTML description

        self.etag = event.get('etag', '')
        self.id = event.get('id', '')
        self.summary = event.get('summary', '')
        self.location = event.get('location', '')
        self.calendar_link = event.get('calendar_link', '') # Link to Google Calendar
        self.created = event.get('created', '')
        self.updated = event.get('updated', '')
        self.creator = event.get('creator', {})
        self.organizer = event.get('organizer', {})
        self.start = event.get('start', {})
        self.end = event.get('end', {})
        self.recurring_event_id = event.get('recurringEventId', '')
        self.original_start_time = event.get('originalStartTime', {})
        self.visibility = event.get('visibility', 'public')
        self.ical_uid = event.get('iCalUID', '')

    def get_social_link(self, event):
        regex = r'(?i)\b((?:[a-z][\w-]+:(?:/{1,3}|[a-z0-9%])|www\d{0,3}[.]|[a-z0-9.\-]+[.][a-z]{2,4}/)(?:[^\s()<>]+|\(([^\s()<>]+|(\([^\s()<>]+\)))*\))+(?:\(([^\s()<>]+|(\([^\s()<>]+\)))*\)|[^\s`!()\[\]{};:\'".,<>?«»“”‘’]))'

        result = re.search(regex, event.get('description'))

        if not result:
            return ('', '')

        description = '<p>' + event['description'][:result.start()].strip().replace('\n', '</p>\n<p>') + '</p>'

        return (description, result.group(0))

class CalEventsMixin(YearMixin, MonthMixin, WeekMixin, DayMixin, DateMixin):
    def get_context_data(self, *args, **kwargs):
        context = {
            'events': self.get_events_from_saved(),
            'recurrence': self.parse_recurrence()
        }
        return context

    def get_events_from_saved(self):
        events_result = {}

        with open('addons/drone_hangar/static/google/calendar.json', 'r') as f:
            events_result = json.loads(f.read())

        events_by_id = {}
        ids_by_date = {}    # Keys should be dates. This is going to be fed straight into the Blackstone UI calendar.
        
        for result_item in events_result:
            event = Event(result_item)

            events_by_id.update({
                event.id: event
            })

            date_string = event.start['dateTime'][0:10]  # We need the first ten characters of the ISO time string. String slicing uses an exclusive range.

            try:
                ids_by_date[date_string].append(event.id)
            except:
                ids_by_date[date_string] = [event.id]
            
        return {
            'events': events_by_id,
            'dates': ids_by_date
        }
    
    def parse_recurrence(self):
        events_result = {}

        with open('addons/drone_hangar/static/google/recurrence.json', 'r') as f:
            events_result = json.loads(f.read())

        recurrence = {}     # Keys should be human-readable recurrence patterns. This is going to be displayed on the Events page in HTML.
        recurrence_lists = {
            'annual': [],
            'monthly': [],
            'weekly': [],
            'daily': []
        }

        for event in events_result:
            rule = {
                'raw': event['recurrence'][0][6:].split(';'),
                # TODO: If I ever upgrade to 3.9, I can change the awkward slicing syntax to `removeprefix('RRULE:')`.
                'freq': '',
                'byday': [],
                'bymonth': [],
                'bymonthday': [],
                'bysetpos': [],
                'count': 0,
                'until': '',
                'interval': 0
            }

            # For each event, generate a tuple with a human-readable description of the recurrence rule, then use dict() to compile them into a dictionary.

            if "FREQ=YEARLY" in rule['raw']:
                rule['freq'] = 'annual'
            elif "FREQ=MONTHLY" in rule['raw']:
                rule['freq'] = 'monthly'
            elif "FREQ=WEEKLY" in rule['raw']:
                rule['freq'] = 'weekly'
            elif "FREQ=DAILY" in rule['raw']:
                rule['freq'] = 'daily'
            else:
                logging.debug('> > > No RRULE repetition type found. Jumping to next event.')

            # RRULE syntax is keyword-based, so we shouldn't care about position here. Just iterate through the list and assign variables as we find them.
            rule_text = ''

            for prop in rule['raw']:
                prop = prop.partition('=')
                if prop[0] == 'BYDAY':
                    rule['byday'] = prop[2].split(',')
                elif prop[0] == 'BYMONTH':
                    rule['bymonth'] = prop[2].split(',')
                elif prop[0] == 'BYMONTHDAY':
                    rule['bymonthday'] = prop[2].split(',')
                elif prop[0] == 'BYSETPOS':
                    rule['bysetpos'] = prop[2].split(',')
                elif prop[0] == 'COUNT':
                    rule['count'] = prop[2]
                elif prop[0] == 'UNTIL':
                    rule['until'] = prop[2]
                elif prop[0] == 'INTERVAL':
                    rule['interval'] = prop[2]

            intervals = {
                0: '', 1: '',
                2: 'Every other',
                3: 'Every third',
                4: 'Every fourth',
                5: 'Every fifth'
            }

            # Day codes can start with the string or with a positive or negative number. The day strings are predictable, so it's easy to find them with the range [-2:].
            days = {
                'SU': 'Sunday', 'MO': 'Monday', 'TU': 'Tuesday',
                'WE': 'Wednesday', 'TH': 'Thursday', 'FR': 'Friday',
                'SA': 'Saturday'
            }

            pos = {
                '-3': '3rd to last',
                '-2': '2nd to last',
                '-1': 'Last',
                '': '',
                **{     # We can save ourselves from having to type numbers.
                    f'{n}': humanize.ordinal(n) for n in range(1,31)
                }
            }

            months = {
                1: 'January', 2: 'February', 3: 'March',
                4: 'April', 5: 'May', 6: 'June',
                7: 'July', 8: 'August', 9: 'September',
                10: 'October', 11: 'November', 12: 'December'
            }

            interval_text = intervals[rule['interval']]

            day_list = [
                f'{pos[d[:-2]]} {days[d[-2:]]}' for d in rule['byday']
            ]
            day_text = ", ".join(
                day_list[:-2] + [", and ".join(day_list[-2:])])

            month_list = [
                months[m] for m in rule['bymonth']
            ]
            month_text = ", ".join(
                month_list[:-2] + [", and ".join(month_list[-2:])])

            setpos_text = ''  # TODO: BYSETPOS is kind of terrible. It's unlikely to actually come up, since it's used for some weird scheduling patterns, so I might be able to get away with half-assing it.

            if rule['freq'] == 'annual':
                # Should usually just be the month.
                if interval_text:
                    interval_text = f'{interval_text} year:'
                rule_text = f'{interval_text} {month_text}'
            elif rule['freq'] == 'monthly':
                # Should usually just be the day with either an interval or a position notifier.
                if interval_text:
                    interval_text = f'{interval_text} month:'
                rule_text = f'{interval_text} {day_text}'
            elif rule['freq'] == 'weekly':
                # Day position shouldn't be a thing here.
                if interval_text:
                    interval_text = f'{interval_text} week:'
                rule_text = f'{interval_text} {day_text}'

            recurrence_lists[rule['freq']].append(
                (rule_text, event['id'])
            )
        
        
        for key, events in recurrence_lists.items():
            recurrence.update({
                    key: defaultdict(list)
                })
            for entry in events:
                recurrence[key][entry[0]].append(entry[1])

                logging.debug(f'{entry[0]} in {key} set to {entry[1]}')

        recurrence = {k: dict(v) for k, v in recurrence.items()}

        return recurrence

class CalendarView(CalEventsMixin, TemplateView):
    template_name = 'calendar.html'

class EventsView(CalEventsMixin, TemplateView):
    template_name = 'events.html'
