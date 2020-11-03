from django.conf.urls import url
from tendenci.apps.site_settings.utils import get_setting

from httpproxy.views import HttpProxy

urlpatterns = [
    url(r'^proxy/(?P<url>.*)$',
        HttpProxy.as_view(
            base_url='https://madmimi.com/p/',
            mode='record'
        )
    ),
]
