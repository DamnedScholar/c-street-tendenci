from django.http import HttpResponseRedirect

from . import Dropbox

def get_redirect(request, **kwargs):
    return HttpResponseRedirect(Dropbox.get_url(Dropbox(), **kwargs))
