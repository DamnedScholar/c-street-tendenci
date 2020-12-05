import os

import mailchimp_transactional as MailchimpTransactional
from mailchimp_transactional.api_client import ApiClientError

def send(**kwargs):
    try:
        mailchimp = MailchimpTransactional.Client(os.environ.get('MAILCHIMP'))
        response = mailchimp.messages.send({"message": kwargs})
        print(response)
    except ApiClientError as error:
        print("An exception occurred: {}".format(error.text))
