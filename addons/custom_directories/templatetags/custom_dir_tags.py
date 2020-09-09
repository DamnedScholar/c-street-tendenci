import collections
import json
import math

import scrapy

from django import template
from django.shortcuts import get_object_or_404
from django.db.models import Q
from django.template.defaultfilters import slugify

from tendenci.apps.photos.models import Image, PhotoSet, AlbumCover, License

from addons.custom_directories.utils.utils import get_images_for_entry

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

@register.filter()
def imgproxy(url, size):
    import base64
    import hashlib
    import hmac
    import textwrap

    from django.contrib.sites.models import Site

    current_site = Site.objects.get_current()
    # TODO: SSL cert doesn't like `www`.
    prefix = "https://eclectic-co.com/imgproxy"

    sizes = {
        "thumb": {
            'resize': 'fill',
            'width': 200,
            'height': 200,
            'gravity': 'sm',
            'enlarge': 0,
            'extension': 'webp'
        },
        "portrait": {
            'resize': 'fill',
            'width': 300,
            'height': 500,
            'gravity': 'sm',
            'enlarge': 0,
            'extension': 'webp'
        },
        "sm-hero": {
            'resize': 'fill',
            'width': 500,
            'height': 400,
            'gravity': 'sm',
            'enlarge': 0,
            'extension': 'webp'
        },
        "hero": {
            'resize': 'fill',
            'width': 1500,
            'height': 400,
            'gravity': 'sm',
            'enlarge': 0,
            'extension': 'webp'
        },
        "front-hero": {
            'resize': 'fill',
            'width': 1500,
            'height': 400,
            'gravity': 'fp:0.32:0.55',
            'enlarge': 0,
            'extension': 'webp'
        },
    }

    options = sizes[size]

    if url[0] in ['\\', '/']:
        url = f"http://eclectic-co.com{url}"

    # TODO: If this were built for reliability and sophistication instead of convenience, it would probably have a check that errors out to a return call that changes the output to an image that conveys the error if the input options aren't formatted correctly.
    # options.update(json.loads("{%s}" % optionsInput))

    key = bytes.fromhex("a780243df2e5c90dd05fbe0ff81b82fe6086f43cf7acd240a2ae76389bc630d419eca9e478c63b5aa6e9da11a1e0a9d7af9a0dc9e840f0e4291ba722ccb647db")
    salt = bytes.fromhex("89367b50dea8a1de807a25df11bdbc81107b54b10f564c617f0509a949e06402e8c842b47a7bfd51c1bd2ca6941b336b5776174edfe415c01cf80793d3b8de0b")

    encoded_url = base64.urlsafe_b64encode(url.encode("utf-8")).rstrip(b"=").decode()
    # You can trim padding spaces to get good-looking url
    encoded_url = '/'.join(textwrap.wrap(encoded_url, 16))

    path = "/{resize}/{width}/{height}/{gravity}/{enlarge}/{encoded_url}.{extension}".format(
        encoded_url=encoded_url,
        resize=options['resize'],
        width=options['width'],
        height=options['height'],
        gravity=options['gravity'],
        enlarge=options['enlarge'],
        extension=options['extension'],
    ).encode()
    digest = hmac.new(key, msg=salt+path, digestmod=hashlib.sha256).digest()

    protection = base64.urlsafe_b64encode(digest).rstrip(b"=")

    url = b'%s/%s%s' % (
        prefix.encode("utf-8"),
        protection,
        path,
    )

    # without / in url
    # /_PQ4ytCQMMp-1w1m_vP6g8Qb-Q7yF9mwghf6PddqxLw/fill/300/300/no/1/aHR0cDovL2ltZy5leGFtcGxlLmNvbS9wcmV0dHkvaW1hZ2UuanBn.png

    # with / in url
    # /MlF9VpgaHqcmVK3FyT9CTJhfm0rfY6JKnAtxoiAX9t0/fill/300/300/no/1/aHR0cDovL2ltZy5l/eGFtcGxlLmNvbS9w/cmV0dHkvaW1hZ2Uu/anBn.png

    return url.decode()

@register.inclusion_tag('airbnb_list.html')
def airbnb():
    with open('addons/drone_hangar/static/airbnb/airbnb_data.json') as f:
        data = f.read()

    rooms = json.loads(data)

    prices = [room['rate'] for room in rooms.values()]

    def divide_chunks(l, n): 
        # looping till length l 
        for i in range(0, len(l), n):  
            yield l[i:i + n] 

    price_tiers = list(divide_chunks(prices, math.ceil(len(prices) / 3)))

    for k, v in rooms.items():
        price_tier = "$" * len([l[-1] for l in price_tiers if l[0] < v['rate']])

        rooms[k].update({
            "sorting": json.dumps({
                "category": "short-term",
                # "filters": [ price_tier, slugify(v['guests']),
                #     slugify(v['beds']), slugify(v['bedrooms']) ],
                "filters": [ price_tier, slugify(v['beds']) ],
                # TODO: Limit the filters we display until I design the UI better so that we can have organized buttons.
                "name": v['name'],
                "rating": v['avg_rating'],
                "rate": v['rate'],
            })
        })

    return { "rooms": rooms }
