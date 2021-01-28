from django.conf.urls import url, include  # noqa: F401
from django.contrib import admin

from django_jinja import views

from . import settings
from lib.trixie_pages.views import UnknownPageView
from tools.modulation.utils import Registry


# Modules are bespoke components core to the application.
lib = Registry('lib')
# Tools are stand-alone scripts that perform auxilliary functions.
tools = Registry('tools')

handler400 = views.BadRequest.as_view()
handler403 = views.PermissionDenied.as_view()
handler404 = UnknownPageView.as_view()
# handler500 = views.ServerError.as_view()

urlpatterns = tools.get_url_patterns() + [
    url(r'', include('%s.urls' % 'httpproxy')),
    url(r'admin/', admin.site.urls),
    # url(r'', include('%s.urls' % 'django.contrib.auth')),
] + lib.get_url_patterns()

if settings.DEBUG:
    import debug_toolbar
    urlpatterns += [
        url(r'^__debug__/', include(debug_toolbar.urls)),
    ]
