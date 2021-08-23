from django.urls import path, re_path, include
from django.contrib import admin
from django.conf import settings
from django.conf.urls.static import static

from wagtail.admin import urls as wagtailadmin_urls
from wagtail.core import urls as wagtail_urls
from wagtail.documents import urls as wagtaildocs_urls

from django_jinja import views

from . import settings
# from lib.pageboy.views import UnknownPageView
from tools.modulation.utils import Registry


# Modules are bespoke components core to the application.
lib = Registry('lib')
# Tools are stand-alone scripts that perform auxilliary functions.
tools = Registry('tools')

handler400 = views.BadRequest.as_view()
handler403 = views.PermissionDenied.as_view()
# handler404 = UnknownPageView.as_view()
# handler500 = views.ServerError.as_view()

urlpatterns = tools.get_url_patterns() + lib.get_url_patterns() + [
    path('proxy/', include('%s.urls' % 'httpproxy')),
    path('admin/', admin.site.urls),
    path('cms/', include(wagtailadmin_urls)),
    path('documents/', include(wagtaildocs_urls)),
    path('', include(wagtail_urls)),
    # url(r'', include('%s.urls' % 'django.contrib.auth')),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

if settings.DEBUG:
    import debug_toolbar
    urlpatterns += [
        path('__debug__/', include(debug_toolbar.urls)),
    ]
