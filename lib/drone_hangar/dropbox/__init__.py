# For relative imports to work in Python 3.6
import os, sys

from fs import copy; sys.path.append(os.path.dirname(os.path.realpath(__file__)))

import logging

logger = logging.getLogger('dropbox-fs')

from django.conf import settings

import arrow
import dropbox
import fs
from fs._bulk import Copier
from fs.copy import copy_fs_if_newer, copy_structure
from fs.mirror import _mirror
from fs.opener import manage_fs
from fs.path import iteratepath
from fs.tools import is_thread_safe
from fs.tree import render
from fs.walk import Walker
import sentry_sdk as sentry

class Dropbox:
    def __init__(self):
        self.oauth = os.environ.get('DROPBOX_OAUTH')
        self.api = dropbox.Dropbox(self.oauth)
        self.fs = fs.open_fs(
            'osfs://' + settings.MEDIA_ROOT + 'dropbox/')
        self.dbfs = fs.open_fs(
            f'dropbox://dropbox.com?access_token={self.oauth}')

    def __del__(self):
        # Ensure opened filesystems are closed.
        self.fs.close()
        self.dbfs.close()

    # To maintain performance, all calls to files should reference the local file tree `self.fs`, which this class will silently attempt to keep in sync with what the Dropbox API returns.

    @property
    def tree(self):
        return render(self.fs, with_color=True)

    def get(self, query='', path='', random=False):
        '''
        Get the first or a random file according to a query parameter and/or path string.
        '''
        file = ''
        if path:
            file = ''

        return file

    def fuzzy_walk(self, query=''):
        results = []
        for file in self.fs.walk.files():
            results.append(file)

        logger.warn(results)
        return results

    def mirror(self):
        '''
        Discreetly copies everything from the remote FS into the local one. This method exists so that Celery can easily call it and not have to worry about PyFilesystem internals.
        '''

        def breadcrumb(src_fs, src_path, dest_fs, dest_path):
            # sentry.add_breadcrumb(  # Record individual files.
            #         crumb={
            #             'message': 
            #             'timestamp': arrow.now()
            #         },
            #         hint={}
            #     )
            logger.info(f'Copied {src_path} on Dropbox to {dest_path} in the local fs.')

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
                # fs.mirror.mirror doesn't allow a function to run on copy.
                self.dbfs,                      # Source
                self.fs,                        # Destination
                workers=2,                      # Threads (0 for single)
            )
            # copy_structure(self.dbfs, self.fs)
            # logger.info('Folders copied.')
            

        logger.warn('The Dropbox has been cloned to the local machine.')

dbx = Dropbox()
