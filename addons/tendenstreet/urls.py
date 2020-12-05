from django.views.generic import TemplateView
from django.conf.urls import url
from .views import gov
from .views.calendar import CalendarView, EventsView

urlpatterns = [
    url(r'^cid/$', gov.cid, name="views.cid"),
    url(r'^events/$', EventsView.as_view(), name="views.events"),
    url(r'^calendar/$', CalendarView.as_view(), name="views.calendar"),
    url(r'^calendar/<int:yyyy>-<int:mm>$', CalendarView.as_view(), name="views.calendar"),
    url(r'lit-hel/', TemplateView.as_view(template_name='lit-hel.html')),
]
