from django.views.generic import TemplateView
from django.conf.urls import url
from tendenci.apps.site_settings.utils import get_setting
from .views.calendar import CalendarView, EventsView
from .views import gov
from .views import document_viewer

# TODO: Do I need this? https://docs.djangoproject.com/en/2.2/topics/http/urls/#registering-custom-path-converters
# class FourDigitYearConverter:
#     regex = '[0-9]{4}'

#     def to_python(self, value):
#         return int(value)

#     def to_url(self, value):
#         return '%04d' % value

# register_converter(FourDigitYearConverter, 'yyyy')

urlpatterns = [
    url(r'^cid/$', gov.cid, name="views.cid"),
    url(r'^events/$', EventsView.as_view(), name="views.events"),
    url(r'^calendar/$', CalendarView.as_view(), name="views.calendar"),
    url(r'^calendar/<int:yyyy>-<int:mm>$', CalendarView.as_view(), name="views.calendar"),
    url(r'communique/', document_viewer.DocumentViewerView.as_view(), name="views.document_viewer")
]
