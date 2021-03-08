from django.test import RequestFactory

from sockpuppet.reflex import Reflex

import logging

logger = logging.getLogger(__name__)


class UserFixedReflex(Reflex):
    # TODO: This is a version of the Reflex class that fixes the `request` property to always present a viable User. It's a deliberate security hole and should be managed appropriately.
    @property
    def request(self):
        factory = RequestFactory()
        request = factory.get(self.url)
        request.session = self.consumer.scope['session']

        from channels.auth import UserLazyObject, get_user_model
        user = self.consumer.scope['user']

        if isinstance(user, UserLazyObject):
            user = get_user_model().objects.all()[1]
            logger.warning('We caught a lazy object and put it to work. If you are seeing this message, make sure that you don\'t have other accounts turned on, because if you do, they can all edit every page.')

        request.user = user

        # request.user = self.consumer.scope['user']
        request.POST = self.params
        return request
