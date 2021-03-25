from django.conf.urls import url

from .dropbox import Dropbox

urlpatterns = [
    url(r'^dropbox/(?P<path>.*)$', Dropbox.get, name='dropbox.get-path'),
    url(r'^dropbox/get/(?P<query>.*)$', Dropbox.get, name='dropbox.get-query'),
    url(r'^dropbox/random/(?P<query>.*)$', Dropbox.get, {'random': True},
        name='dropbox.random'),
]
