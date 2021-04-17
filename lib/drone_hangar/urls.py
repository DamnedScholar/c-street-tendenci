from django.urls import path, re_path

from .dropbox import views

urlpatterns = [
    re_path(r'^dropbox/((?P<segment>.*)/)?get/(?P<query>.*)$',
        views.get_redirect,
        name='dropbox.get-query'),
    re_path(r'^dropbox/((?P<segment>.*)/)?random/(?P<query>.*)$',
        views.get_redirect, {'random': True},
        name='dropbox.random'),
    re_path(r'^dropbox/((?P<segment>.*)/)?(?P<path>.*)$',
        views.get_redirect,
        name='dropbox.get-path'),
]
