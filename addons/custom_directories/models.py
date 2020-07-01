from django.db import models

from addons.drone_hangar.models import AirBnBImage


# class AirBnBData (models.Model):
#     room_id = models.IntegerField(primary_key=True) # AirBnB ID
#     name = models.CharField(max_length=30)
#     timestamp = models.DateTimeField()  # When the spider retrieved the data
#     primary_picture = models.ForeignKey('AirBnBImage', null=True, on_delete=models.SET_NULL, related_name="+")
#     profile_picture = models.ForeignKey('AirBnBImage', null=True, on_delete=models.SET_NULL, related_name="+")

#     lat = models.FloatField()
#     lng = models.FloatField()

#     # Store a list of amenities in the future?

#     avg_rating = models.FloatField()
#     reviews_count = models.IntegerField()

#     rate = models.FloatField()
#     rate_type = models.CharField(max_length=30)

#     verified = models.BooleanField(default=False)
#     super_host = models.BooleanField(default=False)

#     guests = models.CharField(max_length=30, blank=True)
#     baths = models.CharField(max_length=30, blank=True)
#     bedrooms = models.CharField(max_length=30, blank=True)
#     beds = models.CharField(max_length=30, blank=True)
