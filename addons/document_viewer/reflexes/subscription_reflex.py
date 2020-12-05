from sockpuppet.reflex import Reflex

from ..views.subscription import subscribe


class SubscriptionReflex(Reflex):
    def submit(self, email):
        subscribe(email)
