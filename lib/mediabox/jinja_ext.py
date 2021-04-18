from jinja2.ext import Extension
from django_jinja import library

from .core import Mediabox

@library.extension
class MediaboxExtension(Extension):
    def __init__(self, environment):
        '''
        Initalize a Mediabox instance and attach it to the Jinja environment. As this is set up, it will be a different instance than the one imported from the module. All important persistent information gets stored in the attached filesystems.
        '''
        super(MediaboxExtension, self).__init__(environment)
        environment.globals["mediabox"] = Mediabox()
