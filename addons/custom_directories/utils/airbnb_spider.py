import scrapy
import collections
import json
from urllib.parse import urlencode

class AirbnbSpider(scrapy.Spider):
    name = 'airbnb'
    allowed_domains = ['www.airbnb.com']
    start_urls = ['http://www.airbnb.com/']

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
            room['picture_url'] = listing.get('picture_url')
            room['price'] = home.get('pricing_quote').get('rate').get('amount')
            room['avg_rating'] = listing.get('avg_rating')
            room['reviews_count'] = listing.get('reviews_count')

            data_dict[room_id] = room

        yield data_dict