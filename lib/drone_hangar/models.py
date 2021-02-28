from django.db import models
from django.db.models import JSONField


class Archive (models.Model):
    # Create a log of all actions performed by spiders. This will enable lookup and recall operations (in case an API goes down or has a bug and we need to roll back to a previous version of the data) as well as providing proof of the services running.
    guid = models.UUIDField(primary_key=True)
    name = models.CharField(verbose_name="Name of the Spider", max_length=50)
    timestamp = models.DateTimeField(auto_now_add=True)
    payload = JSONField(verbose_name="API Response")
    stats = JSONField(verbose_name="Scrapy Stats")

# I'm using a specialized model for each scraper, with a generic model that they can inherit from. The specialized model has rules for how to associate it with other content, such as AirBnB rooms.

class ScrapedImage (models.Model):
    # This needs to be a basic file storage model to retain information about images scraped from AirBnB and other sources. Some of these we might want to port over to the main site, but ScrapedImages shouldn't necessarily be considered permanent since they might come and go.
    name = models.CharField(max_length=30)
    image = models.ImageField(upload_to='lib/drone-hangar/scrapy/storage')
    timestamp = models.DateTimeField()

class ArchivedScrapedImage (ScrapedImage):
    # Consider a permanent archival model for scraped images that get replaced by a future scraping.
    archive_time = models.DateTimeField()



# class AirBnBImage (ScrapedImage):
#     # pic_id = models.IntegerField(primary_key=True, default=0) # AirBnB ID
#     room = models.ForeignKey('AirBnBData', on_delete=models.CASCADE)
