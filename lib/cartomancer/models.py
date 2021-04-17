from datetime import datetime

from django.contrib.auth.models import User
from django.conf import settings
from django.core.validators import RegexValidator
from django.db import models
from django.contrib.gis.db import models as geom
from django.db.models import JSONField
from django.utils.translation import ugettext_lazy as _

from address.models import AddressField
from partial_date import PartialDateField
from phonenumber_field.modelfields import PhoneNumberField

from modelcluster.fields import ParentalKey

from wagtail.core.fields import StreamField
from wagtail.admin.edit_handlers import FieldPanel, InlinePanel, StreamFieldPanel
from wagtail.core.models import Orderable, Page
from wagtail.search import index
from wagtail.images.edit_handlers import ImageChooserPanel

from lib.pageboy.blocks import BaseStreamBlock
# TODO: https://github.com/wagtail/bakerydemo/blob/master/bakerydemo/base/blocks.py#L53
from lib.chronomancy.choices import DAY_CHOICES

class Contact(Page):
    """
    This represents a person or organization that could be contacted. The `details` property is meant as a freeform data structure to hold information that can't fit into the model. It might sometimes have redundant information, or it could have additional phone numbers.
    """
    details = JSONField(verbose_name="Contact Card", null=True)
    first_name = models.CharField(_("First name"), max_length=255)
    last_name = models.CharField(_("Last name"), max_length=255)
    email = models.EmailField(null=True)
    phone = PhoneNumberField(null=True)
    address = AddressField(null=True)
    account = models.ForeignKey(
        User, related_name="account", on_delete=models.SET_NULL, null=True
    )

class Location(Page):
    # TODO: Locations should be able to be serialized as GeoJSON Feature objects in a FeatureCollection. This means they at least need to store the same data, and I should probably build a `__str__` override that just outputs the correct JSON so that it's effortless on the receiving end.

    def get_slug(self):
        return self.plus

    point = geom.PointField(geography=True,
        default=(-93.29067081212997, 37.230544082999714)
    )
    address = AddressField(related_name="+", blank=True)
    plus = models.CharField(max_length=20, blank=True)

class Contactable:
    """
    This is a mixin to allow for adding contact information to different types of models.
    """
    # Don't allow referenced contacts to be deleted.
    contacts = models.ManyToManyField(Contact, related_name='representing')

    def get_phone(self):
        """
        If there isn't a phone number set when the model is first saved, look in its contacts for phone numbers and add one of them.

        TODO: In the future, I should put in a measure to double-check with a human that the automatically acquired number is the correct one.
        """
        try:
            return self.contacts.first().phone
        except BaseException:
            return ''

    phone = PhoneNumberField(verbose_name='Primary Number', blank=True,
        default=get_phone)

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


class EntitiesIndexPage(Page):
    """
    A Page model that creates an index page (a listview)
    """
    introduction = models.TextField(
        help_text='Text to describe the page',
        blank=True)
    image = models.ForeignKey(
        'wagtailimages.Image',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='+',
        help_text='Landscape mode only; horizontal width between 1000px and 3000px.'
    )

    # Only EntityPage objects can be added underneath this index page
    subpage_types = ['EntityPage']

    # Allows children of this indexpage to be accessible via the indexpage
    # object on templates. We use this on the homepage to show featured
    # sections of the site and their child pages
    def children(self):
        return self.get_children().specific().live()

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
        ImageChooserPanel('image'),
    ]


class EntityPage(Page):
    """
    Detail for a specific bakery entity.
    """
    introduction = models.TextField(
        help_text='Text to describe the page',
        blank=True)
    image = models.ForeignKey(
        'wagtailimages.Image',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='+',
        help_text='Landscape mode only; horizontal width between 1000px and 3000px.'
    )
    body = StreamField(
        BaseStreamBlock(), verbose_name="Page body", blank=True
    )

    map = models.ForeignKey(Location, related_name='entities',
        on_delete=models.PROTECT)

    def get_address(self):
        return self.location.address

    address = AddressField(related_name="+", blank=True,
        default=get_address)

    lat_long = models.CharField(
        max_length=36,
        help_text="Comma separated lat/long. (Ex. 64.144367, -21.939182) \
                   Right click Google Maps and select 'What\'s Here'",
        validators=[
            RegexValidator(
                regex=r'^(\-?\d+(\.\d+)?),\s*(\-?\d+(\.\d+)?)$',
                message='Lat Long must be a comma-separated numeric lat and long',
                code='invalid_lat_long'
            ),
        ]
    )

    contacts = models.ManyToManyField(Contact, related_name='representing')

    # Search index configuration
    search_fields = Page.search_fields + [
        index.SearchField('address'),
        index.SearchField('body'),
    ]

    # Fields to show to the editor in the admin view
    content_panels = [
        FieldPanel('title', classname="full"),
        FieldPanel('introduction', classname="full"),
        ImageChooserPanel('image'),
        StreamFieldPanel('body'),
        FieldPanel('address', classname="full"),
        FieldPanel('lat_long'),
        InlinePanel('hours_of_operation', label="Hours of Operation"),
    ]

    def __str__(self):
        return self.title

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

    # Makes additional context available to the template so that we can access
    # the latitude, longitude and map API key to render the map
    def get_context(self, request):
        context = super(EntityPage, self).get_context(request)
        context['lat'] = self.lat_long.split(",")[0]
        context['long'] = self.lat_long.split(",")[1]
        context['google_map_api_key'] = settings.GOOGLE_MAP_API_KEY
        return context

    # Can only be placed under a EntitiesIndexPage object
    parent_page_types = ['EntitiesIndexPage']
