from datetime import datetime
import json
import random
import re

import arrow

import logging; logger = logging.getLogger('Cartomancer 🗺 ')

from django.apps import apps
from django.contrib.auth.models import User
from django.contrib.gis.db import models as geom
from django.contrib.gis.geos import Point
from django.conf import settings
from django.core import serializers
from django.core.validators import RegexValidator
from django.db import models
from django.forms import ModelForm
from django.utils.translation import ugettext_lazy as _

# from clint.textui import indent, prompt

from address.models import AddressField
from fuzzywuzzy import fuzz
from fuzzywuzzy import process
from partial_date import PartialDateField
from phonenumber_field.modelfields import PhoneNumberField

from modelcluster.fields import ParentalKey, ParentalManyToManyField

from wagtail.core.fields import RichTextField, StreamField
from wagtail.admin.edit_handlers import FieldPanel, FieldRowPanel, InlinePanel, MultiFieldPanel, StreamFieldPanel
from wagtail.core.models import Collection, Orderable, Page
from wagtail.snippets.models import register_snippet
from wagtail.search import index
from wagtail.images.models import Image
from wagtail.images.edit_handlers import ImageChooserPanel

from wagtailgmaps.edit_handlers import MapFieldPanel

from lib.pageboy.models import HeroicPage
from lib.pageboy.blocks import BaseStreamBlock
# TODO: https://github.com/wagtail/bakerydemo/blob/master/bakerydemo/base/blocks.py#L53
from lib.chronomancy.choices import DAY_CHOICES

from .apps import CartomancerConfig


@register_snippet
class Contact_Card(models.Model):
    """
    This represents a person or organization that could be contacted. The `details` property is meant as a freeform data structure to hold information that can't fit into the model. It might sometimes have redundant information, or it could have additional phone numbers.
    """
    details = models.JSONField(verbose_name="Contact Card", null=True)
    first_name = models.CharField(_("First name"), max_length=255)
    last_name = models.CharField(_("Last name"), max_length=255)
    email = models.EmailField(null=True)
    office_phone = PhoneNumberField(null=True)
    cell_phone = PhoneNumberField(null=True)
    address = AddressField(null=True)
    account = models.ForeignKey(
        User, related_name="account", on_delete=models.SET_NULL, null=True
    )

    panels = [
        MultiFieldPanel([
            FieldRowPanel([
                FieldPanel('first_name'),
                FieldPanel('last_name')
            ])
        ], heading="Personal Details"),
        MultiFieldPanel([
            FieldPanel('email'),
            FieldRowPanel([
                FieldPanel('office_phone'),
                FieldPanel('cell_phone')
            ]),
            MapFieldPanel('address')
        ], heading="Contact"),
        FieldPanel('account')
    ]

@register_snippet
class Location_Pin(models.Model):
    # TODO: Locations should be able to be serialized as GeoJSON Feature objects in a FeatureCollection. This means they at least need to store the same data, and I should probably build a `__str__` override that just outputs the correct JSON so that it's effortless on the receiving end.

    coords = geom.PointField(geography=True, null=True, blank=True,
        default='POINT(-93.29067081212997 37.230544082999714)'
    )
    address = AddressField(related_name="+", blank=True,
        on_delete=models.PROTECT
    )
    plus = models.CharField(max_length=20, blank=True)

    panels = [
        MapFieldPanel('coords', latlng=True),
        MapFieldPanel('address'),
        FieldPanel('plus')
    ]

class OperatingHours(models.Model):
    """
    A Django model to capture operating hours for a Entity
    """

    day = models.CharField(
        max_length=4,
        choices=DAY_CHOICES,
        default='MON'
    )
    opening_time = models.TimeField(
        blank=True,
        null=True
    )
    closing_time = models.TimeField(
        blank=True,
        null=True
    )
    closed = models.BooleanField(
        "Closed?",
        blank=True,
        help_text='Tick if entity is closed on this day'
    )

    panels = [
        FieldPanel('day'),
        FieldPanel('opening_time'),
        FieldPanel('closing_time'),
        FieldPanel('closed'),
    ]

    class Meta:
        abstract = True

    def __str__(self):
        if self.opening_time:
            opening = self.opening_time.strftime('%H:%M')
        else:
            opening = '--'
        if self.closing_time:
            closed = self.closing_time.strftime('%H:%M')
        else:
            closed = '--'
        return '{}: {} - {} {}'.format(
            self.day,
            opening,
            closed,
            settings.TIME_ZONE
        )


class EntityOperatingHours(Orderable, OperatingHours):
    """
    A model creating a relationship between the OperatingHours and Entity
    Note that unlike BlogPeopleRelationship we don't include a ForeignKey to
    OperatingHours as we don't need that relationship (e.g. any Entity open
    a certain day of the week). The ParentalKey is the minimum required to
    relate the two objects to one another. We use the ParentalKey's related_
    name to access it from the EntityPage admin
    """
    entity = ParentalKey(
        'EntityPage',
        related_name='hours_of_operation',
        on_delete=models.CASCADE
    )


class EntitiesIndexPage(HeroicPage):
    """
    A Page model that creates an index page (a listview)
    """
    introduction = models.TextField(
        help_text='Text to describe the page',
        blank=True)

    # Only entries and child indices can be added underneath this index page
    subpage_types = ['EntityPage', 'EntitiesIndexPage']

    # Allows children of this indexpage to be accessible via the indexpage
    # object on templates. We use this on the homepage to show featured
    # sections of the site and their child pages
    def directory(self):
        return self.get_children().specific().live()

    templates = {
        'page': 'index_page.html.jinja',
        'listing': 'index_listing.html.jinja'
    }

    # Overrides the context to list all child
    # items, that are live, by the date that they were published
    # http://docs.wagtail.io/en/latest/getting_started/tutorial.html#overriding-context
    def get_context(self, request):
        context = super(EntitiesIndexPage, self).get_context(request)
        context['entities'] = EntityPage.objects.descendant_of(
            self).live().order_by(
            'title')
        return context

    content_panels = Page.content_panels + [
        FieldPanel('introduction', classname="full"),
        ImageChooserPanel('hero'),
    ]


class EntityPage(HeroicPage):
    """
    Detail for a specific directory entity.
    """
    introduction = models.TextField(
        help_text='Text to describe the page',
        blank=True)
    body = RichTextField(blank=True)

    website = models.URLField(blank=True, default='')
    social = models.JSONField(verbose_name="Social media accounts", blank=True, default={})

    data = models.JSONField(blank=True, default={})

    map = models.ForeignKey(Location_Pin, blank=True, null=True,
        related_name='entities', on_delete=models.PROTECT)

    def get_address(self):
        return self.map.address

    address = AddressField(related_name="+", blank=True,
        null=True)

    contacts = ParentalManyToManyField(Contact_Card, related_name='representing', blank=True)

    # Search index configuration
    # search_fields = Page.search_fields + [
    #     index.SearchField('address'),
    #     index.SearchField('body'),
    # ]

    # Fields to show to the editor in the admin view
    content_panels = [
        FieldPanel('title', classname="full"),
        FieldPanel('introduction', classname="full"),
        ImageChooserPanel('hero'),
        FieldPanel('body', classname="full"),
        FieldPanel('address', classname="full"),
        InlinePanel('hours_of_operation', label="Hours of Operation"),
        # InlinePanel('contacts')
    ]

    def __str__(self):
        return self.title

    @property
    def thumbnail(self):
        """
        To find a list of thumbnail candidates, collections can be filtered inexactly against the title of the page (to catch spelling errors).
        """
        colls = []
        q_title = Collection.objects.filter(name__iexact=self.title)
        q_slug = Collection.objects.filter(name__iexact=self.slug)
        # We cast a very broad net to find all collections with a name matching the slug or title of the page. Collections created by Mediabox will have a name matching the name of the subdirectory they came from, so names are not unique.

        colls.append([e for e in q_title])
        colls.append([e for e in q_slug])
        candidates = []

        for coll in colls:
            imgs_for_coll = Image.objects.filter(collection=coll)

            candidates.append(
                [entry.title for entry in imgs_for_coll]
            )

        for query in ['thumbnail', 'directory', self.title]:
            hit = process.extractBests(
                query, candidates, score_cutoff=70)
            
            if hit:
                return Image.objects.get(title__iexact=hit[0])

        consolation = random.choice(candidates)     # Just pick one.
        return Image.objects.get(title__iexact=consolation)

    @property
    def lat_long(self):
        return '0,0'

    @property
    def operating_hours(self):
        hours = self.hours_of_operation.all()
        return hours

    # Determines if the entity is currently open. It is timezone naive
    def is_open(self):
        now = datetime.now()
        current_time = now.time()
        current_day = now.strftime('%a').upper()
        try:
            self.operating_hours.get(
                day=current_day,
                opening_time__lte=current_time,
                closing_time__gte=current_time
            )
            return True
        except EntityOperatingHours.DoesNotExist:
            return False

    templates = {
        'page': 'entity_page.html.jinja',
        'listing': 'entity_listing.html.jinja'
    }

    # Makes additional context available to the template so that we can access
    # the latitude, longitude and map API key to render the map
    def get_context(self, request):
        context = super(EntityPage, self).get_context(request)
        context['lat'] = self.lat_long.split(",")[0]
        context['long'] = self.lat_long.split(",")[1]
        context['google_api_key'] = settings.GOOGLE_API_KEY
        return context

    # Can only be placed under a EntitiesIndexPage object or another entity.
    parent_page_types = ['EntitiesIndexPage', 'EntityPage']

class AirBnBPage(EntityPage):
    '''
    To save on LoC in the data model, data about specific AirBnB units can be kept in the EntityPage.data field. For the most part we only need it when we're filling out the template. We'll also use EntityPage.image and EntityPage.map.
    '''
    templates = {
        'page': 'airbnb_page.html.jinja',
        'listing': 'airbnb_listing.html.jinja'
    }

@register_snippet
class APISource(models.Model):
    title = models.CharField(max_length=255)
    plugin = models.CharField(max_length=255)

    panels = [
        FieldRowPanel([
            FieldPanel('title'),
            FieldPanel('plugin')
        ])
    ]

class APIResult(models.Model):
    timestamp = models.DateTimeField(auto_now_add=True, editable=False)
    source = models.ForeignKey(APISource, blank=True, on_delete=models.PROTECT, related_name='results')
    data = models.JSONField()
    model = models.CharField(max_length=50, blank=True)

    def __str__(self):
        title, model, timestamp = (
            self.source.title,
            self.model,
            arrow.get(self.timestamp).humanize()
        )

        return f"{title} 🢩 {model} 🕰️ {timestamp}"

    def get_model(self):
        cls = apps.get_model(
            app_label="lib.cartomancer", model_name=self.model, require_ready=True)

        return cls


    # TODO: Replace all this with a proper deserialize strategy. https://docs.djangoproject.com/en/3.2/topics/serialization/
    def injest(self):
        for slug, fields in self.data.items():
            cls = this.get_model()

            existing = cls.objects.get(slug=slug)

            template = {
                "model": self.model,
                "fields": fields
            }

            if existing:
                template['pk'] = existing.pk

            fmt = json.dumps()

            obj = serializers.deserialize('json', fmt, ignorenonexistent=True)

