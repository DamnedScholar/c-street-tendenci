from django.conf.urls import url

from .dropbox import views

urlpatterns = [
    url(r'^dropbox/(?P<path>.*)$', views.get_redirect, name='dropbox.get-path'),
    url(r'^dropbox/get/(?P<query>.*)$', views.get_redirect, name='dropbox.get-query'),
    url(r'^dropbox/random/(?P<query>.*)$', views.get_redirect, {'random': True},
        name='dropbox.random'),
]
