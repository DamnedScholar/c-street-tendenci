import os
import shutil

# try:
#     from ..utils import storage_path
# except:
#     from lib.drone_hangar.utils import storage_path

def storage_path(uri):
    path = 'lib/drone_hangar/static'
    check = ''
    p_list = path.split('/')

    p_len = len(p_list)

    while p_len != 0:
        check = '/'.join([p_list[p_len - 1], check])
        if os.path.exists(check):
            result = os.path.join(check, uri)
            print(
                ' '.join([
                    '>>> Storage file populated at', result
                    ])
            )
            return result

        p_len = p_len - 1

    return os.path.abspath(result)

def get_photos():
    # Reach into a specific Dropbox folder and copy over all of the images found there.

    src = "/mnt/c/Users/stick/Dropbox/C-Street Website/Businesses Photos"
    dest = storage_path('dropbox/photos')

    shutil.copytree(src, dest)

if __name__ == "__main__":
    get_photos()
