from django import template
from addons.tendenstreet.views.photoset import PhotosetView

register = template.Library()

def photoset(context, id=0):
    if id == 0:
        return "No photoset specified."

    PhotosetView.as_view(extra_context={'id': id})

register.inclusion_tag('photoset.html', takes_context=True)(photoset)
