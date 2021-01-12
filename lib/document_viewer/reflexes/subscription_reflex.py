from sockpuppet.reflex import Reflex

from ..controllers import subscription
from ..forms import SubscriptionForm


class SubscriptionReflex(Reflex):
    def submit(self):
        form = SubscriptionForm(self.params, auto_id=True)

        if form.is_valid():
            subscription.subscribe(form.cleaned_data['email'])

        # Any instance variables on the Reflex class at the end of the method
        # will get passed into the context. It's likely good practice to avoid
        # setting instance variables until the very end.
        self.form = form
