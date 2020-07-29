from django.conf.urls import url
from tendenci.apps.site_settings.utils import get_setting
from .views.calendar import CalendarView, EventsView

# TODO: Do I need this? https://docs.djangoproject.com/en/2.2/topics/http/urls/#registering-custom-path-converters
# class FourDigitYearConverter:
#     regex = '[0-9]{4}'

#     def to_python(self, value):
#         return int(value)

#     def to_url(self, value):
#         return '%04d' % value

# register_converter(FourDigitYearConverter, 'yyyy')

urlpatterns = [
    url(r'^events/$', EventsView.as_view(), name="views.events"),
    url(r'^calendar/$', CalendarView.as_view(), name="views.calendar"),
    url(r'^calendar/<int:yyyy>-<int:mm>$', CalendarView.as_view(), name="views.calendar"),
]
