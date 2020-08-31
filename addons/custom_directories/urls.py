from django.conf.urls import url
from tendenci.apps.site_settings.utils import get_setting
from . import views

urlpath = "directory"

urlpatterns = [
    # Custom category pages
    # TODO: Clean this up and make the category list pull from a canonical source instead of being hardcoded.
    # url(r'^%s/(?P<cat>(%s))/$' % (urlpath, views.CustomCats().cats_regex()), views.category, name="directory.category"),
    url(r'^directory/(?P<cat>(food-and-drink|shopping|lifestyle|services|venues-and-events|rental))/$', views.category, name="directory.category"),
    url(r'^directory/(?P<cat>(food-and-drink|shopping|lifestyle|services|venues-and-events|rental))/print/$', views.print, name="directory.print"),
    url(r'^(?P<slug>[\w\-\/]+)/$', views.details, name="directory"),
]
