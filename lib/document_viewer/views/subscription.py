import json

from django.core.mail import send_mail
from django.http import HttpResponseRedirect
from django.shortcuts import render

from ..forms import SubscriptionForm
from ..controllers import subscription

# from lib.tendenstreet.mailgun import mailgun

def submitOrDisplay(request):
    print("This is the form.")
    # if this is a POST request we need to process the form data
    if request.method == 'POST':
        # create a form instance and populate it with data from the request:
        form = SubscriptionForm(request.POST)
        # check whether it's valid:
        if form.is_valid():
            email = form.cleaned_data['email']

            subscription.subscribe(email)
            
            return HttpResponseRedirect('/')

    # if a GET (or any other method) we'll create a blank form
    else:
        form = SubscriptionForm(label_suffix='!')
        
        if not request['session']['form']:
            request['session'].update({'form': form})

        with open('form-in.txt', 'w') as f:
            f.write(json.dumps(request['session']))

        print(repr(request['session']))

    return render(request, 'dviewer/subscription.html', {'form': form})
