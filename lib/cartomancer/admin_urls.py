from django.conf.urls import url

from lib.cartomancer.views import sources

app_name = 'cartomancer'

urlpatterns = [
    url(r'^sources/', sources, name='directory_comparison'),
]
