import os

from django.db.models import Q

import fuzzywuzzy
import random
import unicodedata

def get_images_for_entry(query):
    src = 'static/dropbox/photos'
    scan = os.scandir(src)
    folders = [item.name for item in scan if item.is_dir()]

    selection = fuzzywuzzy.process.extractOne(query, folders)
    
    files = os.listdir(os.path.join(src, selection[0]))

    if len(files) == 0:
        return f'{src}/unspecified.jpg'

    choice = random.choice(files)
    return f'{src}/{selection[0]}/{choice}'

def strip_accents(text):
    try:
        text = unicode(text, 'utf-8')
    except NameError: # unicode is a default on python 3 
        pass

    text = unicodedata.normalize('NFD', text)\
           .encode('ascii', 'ignore')\
           .decode("utf-8")

    return str(text)
