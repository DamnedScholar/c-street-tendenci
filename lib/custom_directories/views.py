from datetime import datetime, timedelta
import subprocess
import time
import string
import json
from collections import namedtuple
import random
import os
import logging

from django.shortcuts import render_to_response
from django.template.defaultfilters import slugify

import hashids

from .utils.utils import get_images_for_entry

# Custom category pages
class CustomCats:
    def cats(self):
        Size = namedtuple('Size', ['w', 'h'])
        Focus = namedtuple('Focus', ['x', 'y'])
        cats = {
            'food-and-drink': {
                'hero': 'img/Van Gogh\'s Rotterdam.jpg',
                'size': Size(1100,345),
                'focus': Focus(0.5,0.5),
                'headline': 'Food and Drink'
            },
            'shopping': {
                'hero': 'img/Askinosie.jpg',
                'size': Size(1100,345),
                'focus': Focus(0.5,0.5),
                'headline': 'Shopping'
            },
            'lifestyle': {
                'hero': 'img/Lifestyle.jpg',
                'size': Size(1100,345),
                'focus': Focus(0.5,0.5),
                'headline': 'Professional Services'
            },
            'services': {
                'hero': 'img/Footbridge Plaza and Market Pavilion.jpg',
                'size': Size(1100,345),
                'focus': Focus(0.5,0.5),
                'headline': 'Personal Services'
            },
            'venues': {
                'hero': 'img/Footbridge Plaza and Market Pavilion.jpg',
                'size': Size(1100,345),
                'focus': Focus(0.5,0.5),
                'headline': 'Venues and Events'
            },
            'rentals': {
                'hero': 'img/Classy Loft.jpg',
                'size': Size(1100,345),
                'focus': Focus(0.5,0.5),
                'headline': 'Rentals'
            }
        }
        return cats

    def cats_regex(self):
        return str(list(self.cats().keys())).replace(', ','|').replace('\'','').replace('[','').replace(']','')

def category(request, cat_slug=None, template_name="category.html"):
    
    all_cats = CustomCats().cats()
    hasher = hashids.Hashids('salty cats')
    random.seed()

    # TODO: Shoehorning this into Tendenci's directory system was a mistake because we don't need to be updating individual entries from the website since that would create discontinuity with the Google Sheet, which should be the Source of Truth. Well, "mistake" is harsh. It makes sense and still functions just fine, but it's not an optimal arrangement if I'm trying to reduce reliance on the CMS and use tools that are natural best fits for specific types of data.
    # cat_obj = DirectoryCategory.objects.filter(slug=cat)
    # directories = Directory.objects.filter(Q(sub_cat__in=cat_obj))

    directories_list = []
    directories = {}

    with open('lib/drone_hangar/static/google/directory.json', 'r') as f:
        directories_list = json.loads(f.read())

    directories = {
        hasher.encode(random.randint(1,100000)): d for d in directories_list if slugify(d['category']) == cat_slug
    }

    if cat_slug == "rentals":
        with open('lib/drone_hangar/static/airbnb/airbnb_data.json', 'r') as f:
            directories.update(json.loads(f.read()))

    for i, d in enumerate(directories.keys()):
        picture_url = get_images_for_entry(directories[d].get('name'))
        web = ""

        if directories[d].get('website'):
            web = directories[d].get('website').strip('http://').strip('https://').strip('www.').rstrip('/')

        services = directories[d].get('filters-services')

        directories[d].update({
            'slug': slugify(directories[d]['name']),
            'picture_url': f'http://localhost/{picture_url}',
            'web': web,
            'sorting': json.dumps({
                "category": all_cats[cat_slug]['headline'],
                "filters": {
                    'services': services,
                },
                "sorts": {
                    "name": directories[d]['name']
                }
            })
            })
    
    with open('lib/custom_directories/output.txt', 'w') as f:
        f.write(json.dumps(directories))

    # Get info for sorting.
    sorting_controller = {
        'callToAction': 'Welcome to our searchable directory. Click the buttons or start typing below to find what you seek.',
        'noResultsMsg': 'Looks like there\'s nothing that meets that requirement.'
    }

    context = {
        'cat': cat_slug,
        'hero': all_cats[cat_slug]['hero'],
        'focus': all_cats[cat_slug]['focus'],
        'size': all_cats[cat_slug]['size'],
        'headline': all_cats[cat_slug]['headline'],
        'directories': directories,
        'sorting_controller': sorting_controller,
        'all_cats': all_cats
    }

    context.update({'full_context': context})

    return render_to_resp(request=request, template_name=template_name,
            context=context)

def print(request, cat_slug=None, template_name="print.html"):
    return category(request, cat_slug, template_name)

def details(request, slug, template_name="view.html"):
    context = {}
    return render_to_resp(request=request, template_name=template_name,
            context=context)
