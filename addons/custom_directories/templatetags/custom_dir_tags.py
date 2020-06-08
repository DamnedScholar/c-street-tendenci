from django import template
from django.shortcuts import get_object_or_404
from django.db.models import Q
from addons.tendenstreet.views.photoset import PhotosetView
from tendenci.apps.photos.models import Image, PhotoSet, AlbumCover, License

from addons.custom_directories.utils import get_images_for_entry

register = template.Library()

@register.filter
def social_name(value):
    return value.lstrip('https://www.facebook.com').lstrip('https://www.instagram.com').rstrip('/')