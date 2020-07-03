import collections
import json
import requests
import tempfile
from datetime import datetime, timedelta
from urllib.parse import urlencode
import logging

from django.core import files

import scrapy
from scrapy.spidermiddlewares.httperror import HttpError
from twisted.internet.error import DNSLookupError
from twisted.internet.error import TimeoutError, TCPTimedOutError

from addons.drone_hangar.models import AirBnBData, AirBnBImage

class AirBnBSpider(scrapy.Spider):
    name = 'airbnb'
    # allowed_domains = ['www.airbnb.com']
    # start_urls = ['http://www.airbnb.com/']

    def check_age(self):
        cache = AirBnBData.objects.all()
        try:
            cache_age = (datetime.now() - cache[0].timestamp)

            if cache_age.total_seconds() > timedelta(days=1).total_seconds():
                logging.warning("> > > The spider cache is old and being refreshed.")
                return True
            else:
                logging.warning("> > > The spider cache is fresh and no spider is being summoned.")
                return False
        except IndexError:  # IndexError indicates no cache.
            logging.warning("> > > The spider cache is empty and being populated.")
            return True

    def start_requests(self):
        logging.warning("> > > Making request.")

        raise TypeError

        request = {
            "place_id": "ChIJ21P2rgUrTI8Ris1fYjy3Ms4",
            "query": "Springfield, MO",
            "refinement_paths[]": "/homes",
            "search_type": "section_navigation",
            "ne_lat": "37.2331430104727",
            "ne_lng": "-93.28451191655864",
            "sw_lat": "37.22330188609263",
            "sw_lng": "-93.2968543698235",
            "search_by_map": "true",
            "key": "d306zoyjsyarp7ifhu67rjxn52tv0t20",
        }

        url = urlencode(request)

        url = 'https://www.airbnb.com/api/v2/explore_tabs?' + urlencode(request)

        # yield scrapy.Request(url=url, callback=self.parse)
        yield scrapy.Request(url=url, callback=self.parse, errback=self.errback, dont_filter=True)

    def errback(self, failure):
        # log all failures
        self.logger.error(repr(failure))

        # in case you want to do something special for some errors,
        # you may need the failure's type:

        if failure.check(HttpError):
            # these exceptions come from HttpError spider middleware
            # you can get the non-200 response
            response = failure.value.response
            self.logger.error('HttpError on %s', response.url)

        elif failure.check(DNSLookupError):
            # this is the original request
            request = failure.request
            self.logger.error('DNSLookupError on %s', request.url)

        elif failure.check(TimeoutError, TCPTimedOutError):
            request = failure.request
            self.logger.error('TimeoutError on %s', request.url)
    
    def parse(self, response):
        data = json.loads(response.body)

        logging.warning("> > > Parsing response data.")

        # TODO: This is brittle; the listings section has `"result_type": "listings"` and we should check for that.
        homes = data.get('explore_tabs')[0].get('sections')[2].get('listings')

        BASE_URL = 'https://www.airbnb.com/rooms/'

        data_dict = collections.defaultdict(dict)
        for home in homes:
            room = {}
            listing = home.get('listing')
            room['room_id'] = str(listing.get('id'))
            
            room['url'] = BASE_URL + str(listing.get('id'))
            room['name'] = listing.get('name')
            room['timestamp'] = datetime.now()
            room['picture_url'] = listing.get('picture_url')
            room['contextual_pictures'] = listing.get('contextual_pictures')
            room['profile_picture'] = listing.get('user').get('picture_url')
            
            room['lat'] = listing.get('lat')
            room['lng'] = listing.get('lng')

            room['rate'] = 0
            room['rate_type'] = home.get('pricing_quote').get('rate_type')

            room['avg_rating'] = listing.get('avg_rating')
            room['reviews_count'] = listing.get('reviews_count')

            room['new'] = listing.get('is_new_listing')
            room['verified'] = listing.get('verified').get('enabled')
            room['super_host'] = listing.get('user').get('is_super_host')
            
            room['guests'] = listing.get('guest_label')
            room['baths'] = listing.get('bathroom_label')
            room['bedrooms'] = listing.get('bedroom_label')
            room['beds'] = listing.get('bed_label')

            logging.warning("> > > Saving data for %s." % room['name'])

            data_dict[room['room_id']] = room
            new_room = AirBnBData(**room)
            new_room.save()

            self.collect_images(self, room=new_room,
                pictures=room['pictures'])

        yield data_dict

    def collect_images(self, room=None, pictures=[]):
        for image in pictures:
            # Steam the image from the url
            request = requests.get(image['original_picture'], stream=True)

            # Was the request OK?
            # if request.status_code != requests.codes.ok:
            #     # Nope, error handling, skip file etc etc etc
            #     continue
            
            # Get the filename from the url, used for saving later
            file_name = image['original_picture'].split('/')[-1]
            
            # Create a temporary file
            lf = tempfile.NamedTemporaryFile()

            # Read the streamed image in sections
            for block in request.iter_content(1024 * 8):
                
                # If no more file then stop
                if not block:
                    break

                # Write image block to temporary file
                lf.write(block)

            # Create the model you want to save the image to
            image = AirBnBImage(id=image["id"], room=room,
                name=file_name, image=files.File(lf),
                timestamp=datetime.now())

            # Save the temporary image to the model#
            # This saves the model so be sure that is it valid
            image.save()
