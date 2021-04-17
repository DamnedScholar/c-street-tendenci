from django.http import FileResponse, HttpResponseRedirect
from django.shortcuts import redirect

from . import mediabox

import logging
logger = logging.getLogger()

def get_redirect(request, **kwargs):
    logger.warn(repr(kwargs))

    # url = mediabox.get_relative_url(**kwargs)
    path = mediabox.get(**kwargs)
    file = mediabox.open(path)
    logger.warn(repr(file))
    # TODO: Implement this: https://zetcode.com/django/fileresponse/
    return FileResponse(file.contents, filename=file.basename)
