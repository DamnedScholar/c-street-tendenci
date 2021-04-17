from uuid import uuid4

from django.contrib.auth.models import Group, User
from django.db import models

from wagtail.core.models import Page, PageManager

# TODO: https://blog.khophi.co/extending-django-user-model-userprofile-like-a-pro/


class Team (Page):
    guid = models.UUIDField(default=uuid4, editable=False)

    def serve_preview():
        # TODO: Override.
        pass
