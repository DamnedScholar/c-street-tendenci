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

@register.filter()
def imgproxy(url):
    import base64
    import hashlib
    import hmac
    import textwrap

    from django.contrib.sites.models import Site

    current_site = Site.objects.get_current()
    # TODO: This is a dirty hack to get the imgproxy host and port into the URL. Need to make it less shitty by pointing to a config or something.
    prefix = "https://" + current_site.domain + ":8080"

    options = {
        'resize': 'fill',
        'width': 200,
        'height': 200,
        'gravity': 'sm',
        'enlarge': 0,
        'extension': 'webp'
    }

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
    with open('addons/drone_hangar/storage/airbnb/airbnb_data.json') as f:
        data = f.read()

    return { "rooms": json.loads(data) }
