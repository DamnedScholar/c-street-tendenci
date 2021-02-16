from django.urls import path, re_path

from .views import hammer

urlpatterns = [
    path('hammer', hammer, { 'path': '' }),
    re_path(r'^hammer/(?P<path>.+)', hammer)
]
