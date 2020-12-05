import os
import requests

def send(**options):
    os.environ.update({
        'MAILGUN_URL': 'https://api.mailgun.net/v3/signals.eclectic-co.com/messages',
        'MAILGUN_KEY': '77fe24de1120fc2ec720cbc0c7cf844a-360a0b2c-0281b198'
    })
    url = os.environ['MAILGUN_URL']
    key = os.environ['MAILGUN_KEY']

    return requests.post(
        url,
        auth=("api", key),
        data={"from": options['from_email'],
            "to": options['to'],
            "subject": options['subject'],
            "text": options['html']})
