import logging
import os

from django.conf import settings
from django.conf.urls import include, url


logger = logging.Logger('modulation')

class Registry:
    def __init__(self, module_path):
        self.path_slug = module_path

        try:
            os.listdir(module_path)
            self.path = os.path.abspath(module_path)
        except FileNotFoundError:
            self.path = os.path.join(os.getcwd(), module_path)

    @property
    def directory(self):
        return [ module for module in os.listdir(self.path)
            if os.path.isdir(os.path.join(self.path, module))
            and module not in ['__pycache__']
        ]

    @property
    def modules(self):
        """
        Grabs a list of apps that aren't in INSTALLED_APPS
        """
        modules = []

        custom_modules = sorted(self.directory)
        for module in custom_modules:
            module_package = '.'.join([self.path_slug, module])
            try:
                __import__(module_package)
                modules.append(module_package)
            except ImportError:
                pass

        return modules

    def get_url_patterns(self):
        items = []
        for module in self.modules:
            try:
                __import__('.'.join([module, 'urls']))
                items.append(url(r'', include('%s.urls' % module,)))
            except ImportError:
                pass
        return items
