import collections
import json

import scrapy

from django import template
from django.shortcuts import get_object_or_404
from django.db.models import Q
from addons.tendenstreet.views.photoset import PhotosetView
from tendenci.apps.photos.models import Image, PhotoSet, AlbumCover, License

from addons.custom_directories.utils.utils import get_images_for_entry
from addons.custom_directories.utils.airbnb_spider import AirbnbSpider

register = template.Library()

@register.filter
def social_name(value=""):
    value = value.rstrip('/')

    socials = [
        'facebook.com',
        'instagram.com',
        'tripadvisor.com'
    ]
    targets = [ 'http://', 'https://', 'www.' ]
    targets += socials
    targets += [ '/' ]

    def strip_url_parts(value):
        for t in targets:
            if value.startswith(t):
                value = strip_url_parts(value[len(t):])
        
        return value

    return strip_url_parts(value)

def airbnb_mock():
    with open('addons/custom_directories/utils/airbnb_demo.json') as f:
        data = f.read()

    data = json.loads(data)

    repr(data)

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

@register.inclusion_tag('airbnb_list.html')
def airbnb():
    # spider = new AirbnbSpider()

    # query = spider.start_requests()
    query = airbnb_mock()

    repr(query)

    return { "rooms": query }