from django.views.generic import TemplateView
from django.conf.urls import url
from tendenci.apps.site_settings.utils import get_setting
from .views.calendar import CalendarView, EventsView
from .views import gov, document_viewer

urlpatterns = [
    url(r'^cid/$', gov.cid, name="views.cid"),
    url(r'^events/$', EventsView.as_view(), name="views.events"),
    url(r'^calendar/$', CalendarView.as_view(), name="views.calendar"),
    url(r'^calendar/<int:yyyy>-<int:mm>$', CalendarView.as_view(), name="views.calendar"),
    url(r'communique/', document_viewer.DocumentViewerView.as_view(), name="views.document_viewer"),
    url(r'viewer-demo-skypack/', document_viewer.DocumentViewerView.as_view(), name="views.document_viewer"),
    url(r'viewer-demo-webpack/', document_viewer.WebpackView.as_view(), name="views.document_viewer"),
    url(r'lit-hel/', TemplateView.as_view(template_name='lit-hel.html'))
]
