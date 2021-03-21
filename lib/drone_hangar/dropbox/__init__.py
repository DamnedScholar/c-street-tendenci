# For relative imports to work in Python 3.6
import os, sys; sys.path.append(os.path.dirname(os.path.realpath(__file__)))

import dropbox

class Dropbox:
    def __init__(self):
        self.oauth = os.environ.get['DROPBOX_OAUTH']
        self.api = dropbox.Dropbox(self.oauth)

    @property
    def ls(self):
        return 'Eventually this will list the file tree.'
