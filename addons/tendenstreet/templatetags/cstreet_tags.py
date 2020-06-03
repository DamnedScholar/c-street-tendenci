from django import template
from addons.tendenstreet.views.photoset import PhotosetView

register = template.Library()

def photoset(**kwargs):
    return PhotosetView.as_view(kwargs)

register.inclusion_tag('photoset.html')(photoset)
