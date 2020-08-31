from PyPDF2 import PdfFileMerger, PdfFileReader
from datetime import datetime
import os
import shutil
import subprocess
import re
import logging

# try:
#     from ..utils import storage_path
# except:
#     from addons.drone_hangar.utils import storage_path

def storage_path(uri):
    path = 'addons/drone_hangar/static'
    check = ''
    p_list = path.split('/')

    p_len = len(p_list)

    while p_len != 0:
        check = '/'.join([p_list[p_len - 1], check])
        if os.path.exists(check):
            result = os.path.join(check, uri)
            return result

        p_len = p_len - 1

    return os.path.abspath(result)

# TODO: Conversion code cribbed from https://michalzalecki.com/converting-docx-to-pdf-using-python/
def convert(folder, filename, timeout=None):
    args = ['libreoffice', '--headless', '--convert-to', 'pdf', '--outdir', folder, f'{folder}/{filename}']

    process = subprocess.run(args, stdout=subprocess.PIPE, stderr=subprocess.PIPE, timeout=timeout)
    filename = re.search('-> (.*?) using filter', process.stdout.decode())

    if filename is None:
        raise LibreOfficeError(process.stdout.decode())
    else:
        return filename.group(1)

class LibreOfficeError(Exception):
    def __init__(self, output):
        self.output = output

def merge_minutes():
    src = "/mnt/c/Users/stick/Dropbox/CID-Minutes/"
    folders = os.listdir(src)
    folders.remove("desktop.ini")
    for folder in folders:
        merger = PdfFileMerger()    # A new merger for each folder will ensure no 1516-page files.
        dest = os.path.join(storage_path("dropbox/minutes"), f"{folder}.pdf")

        def listdir():
            return os.listdir(f'{src}/{folder}')

        # Check for and convert any docx files first.
        for filename in listdir():
            if filename.endswith((".doc", ".docx")):
                convert(f'{src}/{folder}', filename)

        for filename in listdir():
            if filename.endswith(".pdf"):
                merger.append(PdfFileReader(
                    open(os.path.join(f'{src}/{folder}', filename), 'rb')))

        merger.write(dest)

if __name__ == "__main__":
    merge_minutes()
