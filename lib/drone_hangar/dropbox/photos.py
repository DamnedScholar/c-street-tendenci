import os
import shutil

from ..daemon import Daemon


class PhotoDaemon (Daemon):
    def get_photos(self):
        # Reach into a specific Dropbox folder and copy over all of the images found there.

        src = "/mnt/c/Users/stick/Dropbox/C-Street Website/Businesses Photos"
        dest = self.storage_path('dropbox/photos')

        shutil.copytree(src, dest)


if __name__ == "__main__":
    daemon = PhotoDaemon()
    daemon.get_photos()
