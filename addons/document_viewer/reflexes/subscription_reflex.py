import json

from sockpuppet.reflex import Reflex

from ..controllers import subscription
from ..forms import SubscriptionForm


class SubscriptionReflex(Reflex):
    def submit(self):
        with open('form-out.txt', 'w') as f:
            f.write(json.dumps(self.params))

        form = SubscriptionForm(self.params)

        if form.is_valid():
            subscription.subscribe(form.cleaned_data['email'])

        if form.has_error('email'):
            self.element.dataset['subscription-error'] = form.errors['email']

        self.form = form
