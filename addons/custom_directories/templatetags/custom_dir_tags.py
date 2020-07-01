import collections
import json

import scrapy

from django import template
from django.shortcuts import get_object_or_404
from django.db.models import Q
from tendenci.apps.photos.models import Image, PhotoSet, AlbumCover, License

from addons.custom_directories.utils.utils import get_images_for_entry
from addons.drone_hangar.scrapy.airbnb_spider import AirBnBSpider

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
    with open('addons/drone_hangar/scrapy/airbnb_demo.json') as f:
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
        room['price'] = "$$$"
        room['avg_rating'] = listing.get('avg_rating')
        room['reviews_count'] = listing.get('reviews_count')
        room['superhost'] = ('SUPERHOST' in listing.get('badges'))

        data_dict[room_id] = room

    with open('addons/custom_directories/roomdict.txt', 'w') as f:
        f.write(repr(data_dict))

    return data_dict

@register.inclusion_tag('airbnb_list.html')
def airbnb():
    # Apparently Django's templates are incompatible with defaultdict, so we need to convert to normal dict
    query = dict(airbnb_mock())

    with open('addons/custom_directories/roomquery.txt', 'w') as f:
        f.write(repr(query))

    return { "rooms": query }
