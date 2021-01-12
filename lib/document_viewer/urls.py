from django.conf.urls import url
from .views import document_viewer, subscription, example

urlpatterns = [
    url(r'communique', document_viewer.CommuniqueView.as_view(), name="views.communique"),
    url(r'subscribe', subscription.submitOrDisplay),
    url(r'example', example.ExampleView.as_view())
]
