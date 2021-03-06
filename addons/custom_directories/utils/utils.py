from django.db.models import Q
from tendenci.apps.photos.models import Image, PhotoSet, AlbumCover, License

import os
import fuzzywuzzy
import random

def get_images_for_entry(query):
    # query_spaceless = query.replace(' ','_')

    # sets = PhotoSet.objects.filter(     # Look up all matching sets
    #     Q(name__icontains=query) | Q(tags__icontains=query_spaceless)
    # )
    # result = Image.objects.filter(      # Look up all matching pictures
    #     Q(title__icontains=query) | Q(tags__icontains=query_spaceless)
    # )

    # for s in sets:
    #     # Grab all images that belong to matching sets and add them to the
    #     # results set, using the union operation to filter out duplicates.
    #     s_photos = Image.objects.filter(photoset=s)
    #     result = result.union(s_photos)
    src = 'static/dropbox/photos'
    scan = os.scandir(src)
    folders = [item.name for item in scan if item.is_dir()]

    selection = fuzzywuzzy.process.extractOne(query, folders)
    
    files = os.listdir(os.path.join(src, selection[0]))

    if len(files) == 0:
        return f'{src}/unspecified.jpg'

    choice = random.choice(files)
    return f'{src}/{selection[0]}/{choice}'

import unicodedata

def strip_accents(text):
    try:
        text = unicode(text, 'utf-8')
    except NameError: # unicode is a default on python 3 
        pass

    text = unicodedata.normalize('NFD', text)\
           .encode('ascii', 'ignore')\
           .decode("utf-8")

    return str(text)
