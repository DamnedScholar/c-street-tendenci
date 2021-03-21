import contextlib
import os
import shutil
import arrow

import dropbox


def get_photos():
    # Given an auth token, iterate through a Dropbox and mirror all of the photos to a local folder with thumbnails in an adjacent folder. This is a long-running function that should be handled asyncronously and managed by a job runner.

    dest = os.path.join(os.getcwd(), "Dropbox/photos")

    dbx = dropbox.Dropbox(os.environ.get('DROPBOX_OAUTH'))

    try:
        user = dbx.users_get_current_account()
    except BaseException:
        raise ValueError

    root = list_folder(dbx, '/C-Street Website')

def list_folder(dbx, folder, subfolder):
    """List a folder.
    Return a dict mapping unicode filenames to
    FileMetadata|FolderMetadata entries.
    """
    path = '/%s/%s' % (folder, subfolder.replace(os.path.sep, '/'))
    while '//' in path:
        path = path.replace('//', '/')
    path = path.rstrip('/')
    try:
        with stopwatch('list_folder'):
            res = dbx.files_list_folder(path)
    except dropbox.exceptions.ApiError as err:
        print('Folder listing failed for', path, '-- assumed empty:', err)
        return {}
    else:
        rv = {}
        for entry in res.entries:
            rv[entry.name] = entry
        return rv

def download(dbx, folder, subfolder, name):
    """Download a file.
    Return the bytes of the file, or None if it doesn't exist.
    """
    path = '/%s/%s/%s' % (folder, subfolder.replace(os.path.sep, '/'), name)
    while '//' in path:
        path = path.replace('//', '/')
    with stopwatch('download'):
        try:
            md, res = dbx.files_download(path)
        except dropbox.exceptions.HttpError as err:
            print('*** HTTP error', err)
            return None
    data = res.content
    print(len(data), 'bytes; md:', md)
    return data

@contextlib.contextmanager
def stopwatch(message):
    """Context manager to print how long a block of code took."""
    t0 = arrow.now()
    try:
        yield
    finally:
        t1 = arrow.now()
        dur = t1 - t0
        print('Total elapsed time for %s: %.3f' % (message, str(dur)))
