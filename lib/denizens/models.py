from uuid import uuid4

from django.contrib.auth.models import Group, User
from django.db import models


class Team (Group):
    guid = models.UUIDField(default=uuid4, editable=False)
    page = models.SlugField()

    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    creator = models.ForeignKey(User, related_name="team_creator",
        null=True, on_delete=models.SET_NULL)
    creator_username = models.CharField(max_length=50, null=True)
    owner = models.ForeignKey(User, related_name="team_owner",
        null=True, on_delete=models.SET_NULL)
    owner_username = models.CharField(max_length=50, null=True)

    # TODO: Implement custom managers for querysets.
    # has_page = PageManager()

    class Meta:
        verbose_name_plural = "Teams"
        ordering = ['name']

    def __str__(self):
        return self.name
