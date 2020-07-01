from django.db import models

from tendenci.apps.photos.models import ImageModel

# from addons.custom_directories.models import AirBnBData


# I'm using a specialized model for each scraper, with a generic model that they can inherit from. The specialized model has rules for how to associate it with other content, such as AirBnB rooms.

class ScrapedImage (models.Model):
    # This needs to be a basic file storage model to retain information about images scraped from AirBnB and other sources. Some of these we might want to port over to the main site, but ScrapedImages shouldn't necessarily be considered permanent since they might come and go.
    name = models.CharField(max_length=30)
    image = models.ImageField(upload_to='addons/drone-hangar/scrapy/storage')
    timestamp = models.DateTimeField()

class ArchivedScrapedImage (ScrapedImage):
    # Consider a permanent archival model for scraped images that get replaced by a future scraping.
    archive_time = models.DateTimeField()

class AirBnBData (models.Model):
    room_id = models.IntegerField(primary_key=True) # AirBnB ID
    name = models.CharField(max_length=30)
    timestamp = models.DateTimeField()  # When the spider retrieved the data
    primary_picture = models.ForeignKey('AirBnBImage', null=True, on_delete=models.SET_NULL, related_name="+")
    profile_picture = models.ForeignKey('AirBnBImage', null=True, on_delete=models.SET_NULL, related_name="+")

    lat = models.FloatField()
    lng = models.FloatField()

    # Store a list of amenities in the future?

    avg_rating = models.FloatField()
    reviews_count = models.IntegerField()

    rate = models.FloatField()
    rate_type = models.CharField(max_length=30)

    verified = models.BooleanField(default=False)
    superhost = models.BooleanField(default=False)

    guests = models.CharField(max_length=30, blank=True)
    baths = models.CharField(max_length=30, blank=True)
    bedrooms = models.CharField(max_length=30, blank=True)
    beds = models.CharField(max_length=30, blank=True)

class AirBnBImage (ScrapedImage):
    room = models.ForeignKey('AirBnBData', on_delete=models.CASCADE)
