import json

from django_sockpuppet.sockpuppet.reflex import Reflex

from ..controllers import subscription
from ..forms import SubscriptionForm


class SubscriptionReflex(Reflex):
    def submit(self, params):
        with open('form-out.txt', 'w') as f:
            f.write(json.dumps(params))

        form = SubscriptionForm(params)

        if form.is_valid():
            subscription.subscribe(form.cleaned_data['email'])

        self.request['session']['form'] = form
