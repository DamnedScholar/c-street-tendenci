from django import template
from addons.tendenstreet.views.photoset import PhotosetView

register = template.Library()

register.inclusion_tag('photoset')(PhotosetView.as_view)
