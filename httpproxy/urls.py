from django.conf.urls import url

from .views import HttpProxy

urlpatterns = [
    url(r'^proxy/(?P<url>.*)$',
        HttpProxy.as_view(
            base_url='https://madmimi.com/p/',
            mode='play'
        )
    ),
    url(r'^proxy-fetch/(?P<url>.*)$',
        HttpProxy.as_view(
            base_url='https://madmimi.com/p/',
            mode='record'
        )
    ),
]
