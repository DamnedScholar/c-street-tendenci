from django.core.mail import send_mail
from django.http import HttpResponseRedirect
from django.shortcuts import render

from ..forms import SubscriptionForm
from ..models import SubscriptionLog

from ..mailgun import mailgun

def submitOrDisplay(request):
    # if this is a POST request we need to process the form data
    if request.method == 'POST':
        # create a form instance and populate it with data from the request:
        form = SubscriptionForm(request.POST)
        # check whether it's valid:
        if form.is_valid():
            email = form.cleaned_data['email']

            subscribe(email)
            
            return HttpResponseRedirect('/')

    # if a GET (or any other method) we'll create a blank form
    else:
        form = SubscriptionForm(label_suffix='!')

    return render(request, 'dviewer/subscription.html', {'form': form})

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

def subscribe(email):
    logSubscription(email)
    sendNotificationEmail(email)
