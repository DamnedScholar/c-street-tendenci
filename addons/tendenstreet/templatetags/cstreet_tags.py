import os
import random

from fuzzywuzzy import fuzz, process

from django import template
from django.shortcuts import get_object_or_404
from django.db.models import Q
from addons.tendenstreet.views.photoset import PhotosetView
from tendenci.apps.photos.models import Image, PhotoSet, AlbumCover, License

from addons.custom_directories.utils.utils import get_images_for_entry

register = template.Library()

@register.inclusion_tag('photoset.html')
def photoset(query=""):
    query_spaceless = query.replace(' ','_')

    sets = PhotoSet.objects.filter(     # Look up all matching sets
        Q(name__icontains=query) | Q(tags__icontains=query_spaceless)
    )
    result = Image.objects.filter(      # Look up all matching pictures
        Q(title__icontains=query) | Q(tags__icontains=query_spaceless)
    )

    for s in sets:
        # Grab all images that belong to matching sets and add them to the
        # results set, using the union operation to filter out duplicates.
        s_photos = Image.objects.filter(photoset=s)
        result = result.union(s_photos)

    return {
        'photos': result,
        'query': query
    }

@register.simple_tag(takes_context=True)
def lookup_event(context, key):
    # Yes, this is a little awkward, but the naming actually makes sense when you're breaking it up and assembling it.
    return context['events']['events'][key]

@register.filter()
def local_hero(title):
    def get_images_for_entry(query):
        query_spaceless = query.replace(' ','_')

        sets = PhotoSet.objects.filter(     # Look up all matching sets
            Q(name__icontains=query) | Q(tags__icontains=query_spaceless)
        )
        result = Image.objects.filter(      # Look up all matching pictures
            Q(title__icontains=query) | Q(tags__icontains=query_spaceless)
        )

        for s in sets:
            # Grab all images that belong to matching sets and add them to the
            # results set, using the union operation to filter out duplicates.
            s_photos = Image.objects.filter(photoset=s)
            result = result.union(s_photos)

        urls = [r.get_large_url() for r in result]

        file_path = 'addons/drone_hangar'
        static_path = 'static/dropbox/photos'

        dropbox = os.listdir(f'{file_path}/{static_path}')
        folder_name = process.extractOne(query, dropbox, scorer=fuzz.partial_ratio)[0]

        listdir = os.listdir(f'{file_path}/{static_path}/{folder_name}')

        urls += [f'{static_path}/{folder_name}/{filename}' for filename in listdir]

        # Return a list of URLs.
        return urls

    result = get_images_for_entry(title)

    return random.choice(result)
