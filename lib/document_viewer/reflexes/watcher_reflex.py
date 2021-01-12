from sockpuppet.reflex import Reflex

from ..models import ViewCountLog


class WatcherReflex(Reflex):
    def recordViewEvent(self):
        # Since the tabs are generated dynamically as custom elements, we can
        # store the URL value for each on the clickable component and treat it
        # as a normal attribute.
        url = self.element.dataset['url']

        ViewCountLog.save(url)
