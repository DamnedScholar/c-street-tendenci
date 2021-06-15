from django.core.exceptions import PermissionDenied
from django.http import HttpResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.utils.translation import ugettext as _

from .models import EntityPage, EntitiesIndexPage, APIResult

def sources(request=None):
    

    return HttpResponse()

def compare_with_source(request=None):
    """
    Match the directory entries already in the database with the source data.
    """
    pass
