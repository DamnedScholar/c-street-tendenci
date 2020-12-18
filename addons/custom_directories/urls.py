from django.conf.urls import url
from . import views

urlpath = "directory"

urlpatterns = [
    # Custom category pages
    # TODO: Clean this up and make the category list pull from a canonical source instead of being hardcoded.
    # url(r'^%s/(?P<cat>(%s))/$' % (urlpath, views.CustomCats().cats_regex()), views.category, name="directory.category"),
    url(r'^(?P<cat_slug>(food-and-drink|shopping|lifestyle|services|venues|rentals))/$', views.category, name="directory.category"),
    url(r'^(?P<cat_slug>(food-and-drink|shopping|lifestyle|services|venues|rentals))/print/$', views.print, name="directory.print"),
]
