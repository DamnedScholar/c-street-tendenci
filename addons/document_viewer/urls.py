from django.conf.urls import url
from .views import document_viewer, subscription

urlpatterns = [
    url(r'communique/', document_viewer.CommuniqueView.as_view(), name="views.communique"),
    url(r'subscribe/', subscription.submitOrDisplay),
    url(r'viewer-demo-skypack/', document_viewer.DocumentViewerView.as_view(), name="views.document_viewer"),
    url(r'viewer-demo-webpack/', document_viewer.CommuniqueView.as_view(), name="views.document_viewer")
]
