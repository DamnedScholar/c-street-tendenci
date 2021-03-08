from uuid import uuid4

from django.db import models

import arrow


class GUID (models.Model):
    '''
    Making GUID its own model allows for listing and comparing all objects that have them, which might be a valuable tool for observing the scope of the site. GUIDs should never change and be protected from deletion unless the models they're associated with get deleted.

    This can be thought of as a unique address across the whole site that, unlike a slug, cannot change.
    '''
    guid = models.UUIDField(primary_key=True, default=uuid4, editable=False)

    # When `object.id` is fed into a function that expects a string, let it return its UUID as a string so that it serializes naturally and can be printed without having to introspect the object.
    def __str__(self):
        return f'{self.guid}'

    # When `object.id` is compared with a string, opaquely check against the UUID value and return the result of that.
    def __eq__(self, other):
        return True if self.guid == other else False


class Slug (models.Model):
    '''
    Slugs are the primary means for organizing dynamic means of entry into the site. Slugs should be unique across the whole site, but they can change at any time. Abandoned slugs should hang around unless deleted on purpose. Slugs that have pages attached should not be deleted because that would result in orphaned pages, and it's probably best to protect them from deletion.

    Some models will want to autogenerate slugs and some will want slugs based on user input.
    '''
    slug = models.SlugField()

    # TODO: Keep a history of GUIDs associated with this slug.
