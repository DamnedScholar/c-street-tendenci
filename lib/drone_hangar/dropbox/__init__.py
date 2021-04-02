# For relative imports to work in Python 3.6
import os, sys

import jinja2; sys.path.append(os.path.dirname(os.path.realpath(__file__)))

import logging

logger = logging.getLogger('dropbox-fs')

from random import choice, choices, sample

from django.conf import settings
from django.http import HttpResponseRedirect

import arrow

from django_jinja import library as jinja_library
from jinja2.ext import Extension

import dropbox
import fs
from fs._bulk import Copier
from fs.copy import copy_file_if_newer, copy_fs_if_newer, copy_structure
from fs.errors import DirectoryExpected, DirectoryExists, ResourceNotFound
from fs.mirror import _mirror
from fs.opener import manage_fs
from fs.path import basename, iteratepath, relpath
from fs.tools import is_thread_safe
from fs.tree import render
from fs.walk import Walker

from fuzzywuzzy import process

import sentry_sdk as sentry

class Mediabox:
    def __init__(self):
        '''
        Mediabox is a class that integrates the Django media folder with Dropbox. The class has the ability to mirror the Dropbox folder to the local server and then serve files locally that were deposited by people with no access to the site.
        '''
        self.local_root = os.path.join(settings.MEDIA_ROOT, 'dropbox/')
        self.local_url = os.path.join(settings.MEDIA_URL, 'dropbox/')
        self.oauth = os.environ.get('DROPBOX_OAUTH')
        self.api = dropbox.Dropbox(self.oauth)
        self.fs = fs.open_fs(f'osfs://{self.local_root}')
        self.dbfs = fs.open_fs(
            f'dropbox://dropbox.com?access_token={self.oauth}')

        self._index()

    def __del__(self):
        # Ensure opened filesystems are closed.
        self.fs.close()
        self.dbfs.close()

    # To maintain performance, all calls to files should reference the local file tree `self.fs`, which this class will silently attempt to keep in sync with what the Dropbox API returns.

    @property
    def tree(self):
        (dirs, files) = render(self.fs, with_color=True, file=None)
        return f'Found {dirs} directories and {files} files.'

    def fuzz(self, query):
        return [
            e[0] for e in
            process.extractWithoutOrder(
                query, self.index, score_cutoff=90)
            ]

    def get(self, query='', path='', random=False):
        '''
        Get the first or a random file according to a query parameter and/or path string.
        '''
        if path and path in self.index:
            return path
        elif not random:
            return process.extractOne(query, self.index)[0]
        else:
            return choice(self.fuzz(query))

    def urlize(self, path):
        '''
        Take a PyFS path and convert it into a URL accessible from the outside.
        '''
        return os.path.join(self.local_url, path)

    def get_relative_url(self, **kwargs):
        '''
        Get a specific path or query result in a URL form from the perspective of the HTTP server, which is the path at which the file is accessible from the outside world.
        '''
        return self.urlize(self.get(**kwargs))

    def fuzzy_clump(self, query='', max=6):
        return choices(self.fuzz(query), k=max)

    def get_url_list(self, query='', max=6):
        '''
        Return a list of urls matching the query parameters.
        '''
        return [self.urlize(url) for url in self.fuzzy_clump(query, max)]

    def downstream(self, paths, walker=None):
        '''
        Call this method to syncronize a specific set of files from Dropbox to the local server.
        '''

        for path in paths:
            logger.warn(f'Checking out {path}.')

            if copy_file_if_newer(self.dbfs, path, self.fs, path):
                logger.warn(f'Copied {path} on Dropbox to the local fs.')

        return True

    def upstream(self, paths, walker=None):
        '''
        Call this method to syncronize a specific set of files from the local server to Dropbox.
        '''
        for path in paths:
            logger.warn(f'Checking out {path}.')

            if copy_file_if_newer(self.fs, path, self.dbfs, path):
                logger.warn(f'Copied {path} to the dropbox.')

        return True

    def work_dir(self, path):
        '''
        Take a path and return a filesystem object, making the directory if necessary, in order to isolate work performed on specific folders.
        '''
        try:
            return self.fs.makedir(path)
        except DirectoryExists:
            return self.fs.opendir(path)

    def mirror(self):
        '''
        Discreetly copies everything from the remote FS into the local one. This method exists so that Celery can easily call it and not have to worry about PyFilesystem internals.
        '''
        walker=None

        def breadcrumb(src_fs, src_path, dest_fs, dest_path):
            # If Sentry is integrated correctly, logging calls below Error
            # are added as breadcrumbs to submitted transactions.
            logger.info(
                f'Copied {src_path} on Dropbox to {dest_path} in the local fs.'
            )

        # Overriding this method from PyFilesystem so that we can run a
        # lifecycle callback whenever a file is copied.
        def mirror(
            src_fs,  # type: Union[FS, Text]
            dst_fs,  # type: Union[FS, Text]
            walker=None,  # type: Optional[Walker]
            copy_if_newer=True,  # type: bool
            workers=0,  # type: int
            ):    # type: (...) -> None
            """Mirror files / directories from one filesystem to another.
            Mirroring a filesystem will create an exact copy of ``src_fs`` on
            ``dst_fs``, by removing any files / directories on the destination
            that aren't on the source, and copying files that aren't.
            Arguments:
                src_fs (FS or str): Source filesystem (URL or instance).
                dst_fs (FS or str): Destination filesystem (URL or instance).
                walker (~fs.walk.Walker, optional): An optional walker instance.
                copy_if_newer (bool): Only copy newer files (the default).
                workers (int): Number of worker threads used
                    (0 for single threaded). Set to a relatively low number
                    for network filesystems, 4 would be a good start.
            """
            def src():
                return manage_fs(src_fs, writeable=False)

            def dst():
                return manage_fs(dst_fs, create=True)

            with src() as _src_fs, dst() as _dst_fs:
                with _src_fs.lock(), _dst_fs.lock():
                    _thread_safe = is_thread_safe(_src_fs, _dst_fs)
                    with Copier(num_workers=workers if _thread_safe else 0) as copier:
                        def on_copy(*args):
                            breadcrumb(*args)
                            return copier.copy(*args)

                        _mirror(
                            _src_fs,
                            _dst_fs,
                            walker=walker,
                            copy_if_newer=copy_if_newer,
                            copy_file=on_copy,
                        )

        with sentry.start_transaction(name='Automirror Dropbox') as watcher:
            mirror(
                self.dbfs,          # Source
                self.fs,            # Destination
                walker=walker,      # Optional Walker
                workers=2,          # Threads (0 for single)
            )

            logger.info('Dropbox cloned. Building search index...')

            self._index()

            logger.info('Index complete.')

            return True             # Transaction ends with a positive result.

    class MediaWalker(Walker):
        '''
        Take a dict of config variables to define a PyFS Walker, and then return the instantiated Walker. This is to be used as a convenience function to allow creating arbitrary Walkers without having to use PyFS imports outside this file: anything that uses Mediabox to get files will be able to quickly define Walker behavior.
        '''
        pass

    def _index(self):
        '''
        Iterate through the local mirror and build a list of all files that can be efficiently searched. These files are stored as relative paths because other functions use `os.path.join()`, which has specific behavior around absolute paths.
        '''
        results = []

        for file in self.fs.walk.files():
            results.append(relpath(file))

        self.index = results

@jinja_library.extension
class MediaboxExtension(Extension):
    def __init__(self, environment):
        super(MediaboxExtension, self).__init__(environment)
        environment.globals["mediabox"] = Mediabox()

mediabox = Mediabox()
