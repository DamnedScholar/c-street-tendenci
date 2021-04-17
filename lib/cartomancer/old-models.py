from django.contrib.auth.models import User
from django.contrib.gis.db import models as geom
from django.db import models
from django.db.models import JSONField
from django.utils.translation import ugettext_lazy as _

from address.models import AddressField
from partial_date import PartialDateField
from phonenumber_field.modelfields import PhoneNumberField

from lib.sitemapper.models import GUID, Slug


# TODO: I seem to have fucked up the database tables for this one, somehow. I need to take a deep dive on learning how to unfuck them, but that is a project for a future time because it's not something I can show to Connie on Tuesday.


class Entity(models.Model):
    """
    An entity is anything we might want to @mention.
    """
    guid = models.ForeignKey(GUID, related_name="entity", on_delete=models.PROTECT)
    slug = models.ForeignKey(Slug, related_name="route", on_delete=models.PROTECT)
    name = models.CharField(max_length=50)
    description = models.TextField(blank=True)
    
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    data = JSONField(blank=True)


class Contact(Entity):
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
    created_on = models.DateTimeField(_("Created on"), auto_now_add=True, editable=False)


class Location(Entity):
    # TODO: Locations should be able to be serialized as GeoJSON Feature objects in a FeatureCollection. This means they at least need to store the same data, and I should probably build a `__str__` override that just outputs the correct JSON so that it's effortless on the receiving end.
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


class Addressable:
    """
    This is a mixin for adding address information to different types of models.
    """
    # Don't allow referenced locations to be deleted.
    location = models.ManyToManyField(Location, related_name='entities')

    def get_address(self):
        return self.location.address

    address = AddressField(related_name="+", blank=True,
        default=get_address)


class Company(Entity, Addressable, Contactable):
    """
    This is the main model for directory entities.
    """
    open_since = PartialDateField(blank=True)


class AirBnB(Entity, Addressable, Contactable):
    """
    This is the model for short-term rentals scraped from AirBnB.
    """
    room_id = models.IntegerField(default=0) # AirBnB ID
    # primary_picture = models.ForeignKey('AirBnBImage', null=True, on_delete=models.SET_NULL, related_name="+")
    # profile_picture = models.ForeignKey('AirBnBImage', null=True, on_delete=models.SET_NULL, related_name="+")

    # Store a list of amenities in the future?

    # avg_rating = models.FloatField()
    # reviews_count = models.IntegerField()

    # rate = models.FloatField()
    # rate_type = models.CharField(max_length=30)

    # verified = models.BooleanField(default=False)
    # superhost = models.BooleanField(default=False)

    # guests = models.CharField(max_length=30, blank=True)
    # baths = models.CharField(max_length=30, blank=True)
    # bedrooms = models.CharField(max_length=30, blank=True)
    # beds = models.CharField(max_length=30, blank=True)
