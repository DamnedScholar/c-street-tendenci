from django import template
from addons.tendenstreet.views.photoset import PhotosetView

register = template.Library()

def photoset():
    return PhotosetView.as_view()

register.inclusion_tag('photoset.html')(photoset)
