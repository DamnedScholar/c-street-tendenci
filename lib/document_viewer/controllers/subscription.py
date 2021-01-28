from django.core.mail import send_mail

from ..forms import SubscriptionForm
from ..models import SubscriptionLog

# from lib.puppet_show.mailgun import mailgun


# Entry point.
def subscribe(email):
    logSubscription(email)
    sendNotificationEmail(email)

# "Private" methods.
def logSubscription(email):
    log = SubscriptionLog(email=email)
    log.save()

def sendNotificationEmail(email):
    recipients = ['ChefHolland@hey.com', 'stickfigureonfire@gmail.com']

    # TODO: Mail is turned off at the moment for testing purposes. If it gets turned on and doesn't work, the most likely cause is that the environment variables need to be injected.
    # response = mailgun.send(
    #     subject='New Subscriber',
    #     html=f'Please add {email} to the subscription list.',
    #     from_email='NewsletterDaemon@signal.eclectic-co.com',
    #     to=recipients
    # )
