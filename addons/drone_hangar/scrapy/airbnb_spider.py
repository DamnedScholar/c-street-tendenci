import scrapy
import collections
import json
from datetime import datetime, timedelta
from urllib.parse import urlencode
import logging

from addons.drone_hangar.models import AirBnBData

class AirBnBSpider(scrapy.Spider):
    name = 'airbnb'
    allowed_domains = ['www.airbnb.com']
    start_urls = ['http://www.airbnb.com/']

    def check_age(self):
        cache = AirBnBData.objects.all()
        cache_age = (datetime.now() - cache[0].timestamp)

        if cache_age.total_seconds() > timedelta(days=1).total_seconds():
            logging.debug("> > > The spider cache is old and being refreshed.")
            return True
        else:
            logging.debug("> > > The spider cache is fresh and no spider is being summoned.")
            return False

    def start_requests(self):
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

        yield scrapy.Request(url=url, callback=self.parse)
    
    def parse(self, response):
        data = json.loads(response.body)

        homes = data.get('explore_tabs')[0].get('sections')[2].get('listings')

        BASE_URL = 'https://www.airbnb.com/rooms/'

        data_dict = collections.defaultdict(dict)
        for home in homes:
            room = {}
            listing = home.get('listing')
            room_id = str(listing.get('id'))
            
            room['url'] = BASE_URL + str(listing.get('id'))
            room['name'] = listing.get('name')
            room['timestamp'] = datetime.now()
            room['picture_url'] = listing.get('picture_url')
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

            data_dict[room_id] = room
            record = AirBnBData(**room)
            record.save()

        yield data_dict
