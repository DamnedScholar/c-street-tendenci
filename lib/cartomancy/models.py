from uuid import uuid4

from django.db import models
from django.contrib.postgres.fields import JSONField

from address.models import AddressField
from django_hashids import HashidsField
from partial_date import PartialDateField
from phonenumber_field.modelfields import PhoneNumberField

class Entity (models.Model):
    guid = models.UUIDField(primary_key=True, default=uuid4, editable=False)
    hashid = HashidsField(real_field_name=guid)
    slug = models.SlugField(blank=True)
    name = models.CharField(max_length=50)
    description=models.TextField(blank=True)
    
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    data = JSONField()

class Contact (Entity):
    card = JSONField(verbose_name="Contact Card")

class Location (Entity):
    lat = models.FloatField(blank=True)
    lng = models.FloatField(blank=True)
    address = AddressField(related_name="+", blank=True)
    plus = models.CharField(max_length=20, blank=True)

class Contactable:
    # Don't allow referenced contacts to be deleted.
    contact = models.ManyToManyField(Contact, related_name='entities')

    def get_phone(self):
        return self.contact.card.phone

    phone = PhoneNumberField(verbose_name='Primary Number', blank=True,
        default=get_phone)

class Addressable:
    # Don't allow referenced locations to be deleted.
    location = models.ManyToManyField(Location, related_name='entities')

    def get_address(self):
        return self.location.address

    address = AddressField(related_name="+", blank=True,
        default=get_address)

class Business (Entity, Addressable, Contactable):
    open_since = PartialDateField(blank=True)

class AirBnB (Entity, Addressable, Contactable):
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
