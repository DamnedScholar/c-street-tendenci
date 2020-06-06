from django.conf.urls import url
from tendenci.apps.site_settings.utils import get_setting
from . import views

urlpath = get_setting('module', 'directories', 'url')
if not urlpath:
    urlpath = "directories"

urlpatterns = [
    # Custom category pages
    # url(r'^%s/(?P<cat>(%s))/$' % (urlpath, views.CustomCats().cats_regex()), views.category, name="directory.category"),
    url(r'^%s/(?P<cat>(food-and-drink|shopping|lifestyle|personal-services|venues-and-events|rentals|professionals))/$' % (urlpath), views.category, name="directory.category"),
]
