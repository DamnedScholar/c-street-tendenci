from datetime import datetime, timedelta
import subprocess
import time
import string
import json
from collections import namedtuple
import random

from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404
from django.http import HttpResponseRedirect, HttpResponse, Http404
from django.core.files.storage import default_storage
from django.core.files.base import ContentFile
from django.urls import reverse
from django.contrib import messages
from django.template.defaultfilters import slugify
import simplejson
from django.views.decorators.csrf import csrf_exempt
from django.utils.html import escape
from django.utils.translation import ugettext_lazy as _
from django.db.models import Q

from tendenci.libs.utils import python_executable
from tendenci.apps.site_settings.utils import get_setting
from tendenci.apps.base.decorators import password_required
from tendenci.apps.base.http import Http403
from tendenci.apps.base.views import file_display
from tendenci.apps.perms.decorators import is_enabled
from tendenci.apps.perms.utils import (get_notice_recipients,
    has_perm, has_view_perm, get_query_filters, update_perms_and_save)
from tendenci.apps.event_logs.models import EventLog
from tendenci.apps.meta.models import Meta as MetaTags
from tendenci.apps.meta.forms import MetaForm
from tendenci.apps.theme.shortcuts import themed_response as render_to_resp

from tendenci.apps.directories.models import Directory, DirectoryPricing
from tendenci.apps.directories.models import Category as DirectoryCategory
from tendenci.apps.directories.forms import (DirectoryForm, DirectoryPricingForm,
                                               DirectoryRenewForm, DirectoryExportForm)
from tendenci.apps.directories.utils import directory_set_inv_payment, is_free_listing
from tendenci.apps.notifications import models as notification
from tendenci.apps.base.utils import send_email_notification
from tendenci.apps.directories.forms import DirectorySearchForm

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
                'headline': 'Lifestyle'
            },
            'services': {
                'hero': 'img/Footbridge Plaza and Market Pavilion.jpg',
                'size': Size(1100,345),
                'focus': Focus(0.5,0.5),
                'headline': 'Personal Services'
            },
            'venues-and-events': {
                'hero': 'img/Footbridge Plaza and Market Pavilion.jpg',
                'size': Size(1100,345),
                'focus': Focus(0.5,0.5),
                'headline': 'Venues and Events'
            },
            'rental': {
                'hero': 'img/Classy Loft.jpg',
                'size': Size(1100,345),
                'focus': Focus(0.5,0.5),
                'headline': 'Rentals'
            }
        }
        return cats

    def cats_regex(self):
        return str(list(self.cats().keys())).replace(', ','|').replace('\'','').replace('[','').replace(']','')

@is_enabled('directories')
def category(request, cat=None, template_name="category.html"):
    
    all_cats = CustomCats().cats()

    # TODO: Shoehorning this into Tendenci's directory system was a mistake because we don't need to be updating individual entries from the website since that would create discontinuity with the Google Sheet, which should be the Source of Truth. Well, "mistake" is harsh. It makes sense and still functions just fine, but it's not an optimal arrangement if I'm trying to reduce reliance on the CMS and use tools that are natural best fits for specific types of data.
    # cat_obj = DirectoryCategory.objects.filter(slug=cat)
    # directories = Directory.objects.filter(Q(sub_cat__in=cat_obj))

    directories = []

    with open('addons/drone_hangar/static/google/directory.json', 'r') as f:
        directories = json.loads(f.read())

    directory_images = [
        get_images_for_entry(d['name']) for d in directories
    ]
    # directory_tags = set([  # TODO: Look real hard at this. It probably wants to be changed.
    #     d['tags'] for d in directories
    # ])
    # Convert queryset to list of dicts.
    # directories_firm = list(directories.values())
    for i, d in enumerate(directories):
        image_url = ""
        website = ""

        if directory_images[i]:
            image_url = random.choice(directory_images[i])
            # TODO: This shouldn't be random in production.

        if d.get('website'):
            website = d.get('website').strip('http\:\/\/').strip('https\:\/\/').strip('www.').rstrip('/')

        d.update({
            'slug': slugify(d['name']),
            'image': image_url,
            'website_display': website
            })

    # Get info for sorting.
    sorting_controller = {
        'cta': 'Welcome to our searchable directory. Click the buttons or start typing below to find what you seek.',
        'categories': [],
        'filters': [],
        'sorts': []
    }

    context = {
        'cat': cat,
        'hero': all_cats[cat]['hero'],
        'focus': all_cats[cat]['focus'],
        'size': all_cats[cat]['size'],
        'headline': all_cats[cat]['headline'],
        'directories': directories,
        'directory_images': directory_images,
        'sorting_controller': sorting_controller,
        # 'directory_tags': directory_tags,
        'all_cats': all_cats
    }

    return render_to_resp(request=request, template_name=template_name,
            context=context)

@is_enabled('directories')
def print(request, cat=None, template_name="print.html"):
    all_cats = CustomCats().cats()

    cat_obj = DirectoryCategory.objects.filter(slug=cat)
    directories = Directory.objects.filter(Q(sub_cat__in=cat_obj))

    directories_firm = list(directories.values())

    context = {
        'cat': cat,
        'hero': all_cats[cat]['hero'],
        'focus': all_cats[cat]['focus'],
        'size': all_cats[cat]['size'],
        'headline': all_cats[cat]['headline'],
        'directories': directories_firm,
    }

    return render_to_resp(request=request, template_name=template_name,
            context=context)

def details(request, slug, template_name="view.html"):
    context = {}
    return render_to_resp(request=request, template_name=template_name,
            context=context)
