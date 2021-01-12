#
# This file is ignored unless "ROOT_URLCONF = 'conf.urls'" is configured in
# settings.py
#

from django.conf.urls import url, include  # noqa: F401
from . import settings

from tools.modulation.utils import Registry
# Modules are bespoke components core to the application.
lib = Registry('lib')
# Tools are stand-alone scripts that perform auxilliary functions.
tools = Registry('tools')

# urlpatterns = lib.get_url_patterns() + tools.get_url_patterns()

urlpatterns = lib.get_url_patterns() + [url(r'', include('%s.urls' % 'httpproxy'))]

if settings.DEBUG:
    import debug_toolbar
    urlpatterns += [
        url(r'^__debug__/', include(debug_toolbar.urls)),
    ]
