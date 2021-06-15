from __future__ import absolute_import, unicode_literals

from django.conf.urls import include, url
from django.contrib.admin.utils import quote

from django.urls import reverse

from django.utils.translation import ugettext_lazy as _
from wagtail.contrib.modeladmin.helpers import ButtonHelper
from wagtail.contrib.modeladmin.options import ModelAdmin, modeladmin_register
from wagtail.contrib.modeladmin.views import CreateView, EditView

from wagtail.core import hooks

from . import admin_urls

@hooks.register('register_admin_urls')
def register_admin_urls():
    return [
        url(r'^cartomancer/', include(admin_urls, namespace='cartomancer')),
    ]
