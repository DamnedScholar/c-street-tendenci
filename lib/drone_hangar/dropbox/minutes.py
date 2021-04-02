from datetime import datetime
import os
import shutil
import subprocess
import re
import logging

logger = logging.getLogger()

from celery import shared_task
from pikepdf import Pdf
from PyPDF2 import PdfFileMerger, PdfFileReader

from . import mediabox

@shared_task
def compile_minutes():
    '''
    Using the directory of minutes documents from Dropbox, walk through each directory and concatenate all PDFs. Output the merged files, named identically to the directories they came from, into the root directory, then use the exposed PyFS API on the Mediabox object to upload the new files.
    '''

    # TODO: The full loop has been tested to completion. It just needs to be set up to run automatically on server start and react to a webhook to notify it about updates. Additional flow control should also be put in to make calls to the server only for new files, and to only create PDFs from changed directories. With how rarely this script runs, such performance tweaks aren't high priorities.

    # First we make sure that the requested part of the filesystem is up to date.
    walker = mediabox.MediaWalker(
        filter_dirs=['CID Minutes*'],
    )
    results = [entry for entry
        in mediabox.dbfs.glob('CID-Minutes/**/*.pdf', path='/CID-Minutes/')]

    download_paths = [entry.path for entry in results]
    
    if mediabox.downstream(download_paths):
        logger.warn(f'Minutes synced.')
    else:
        logger.warn(f'We done fucked up.')
    
    # Then we take a list of folders that match our walker.
    dirs = [entry for entry in walker.dirs(mediabox.fs, path=f'/CID-Minutes')]

    with mediabox.work_dir(f'CID-Minutes/out') as outputfs:
        for dirpath in sorted(dirs):
            out = Pdf.new()

            dirname = mediabox.fs.getinfo(dirpath).name

            files = [file for file in walker.files(mediabox.fs, path=dirpath)]

            for file in sorted(files):
                file = mediabox.fs.getsyspath(file)
                src = Pdf.open(file)
                out.pages.extend(src.pages)

            out.save(outputfs.getsyspath('') + f'/{dirname}.pdf')

            mediabox.upstream([f'/CID-Minutes/out/{dirname}.pdf'])   # Needs to take a list.

    return dirs

def storage_path(uri):
    path = "lib/drone_hangar/static"
    check = ""
    p_list = path.split("/")

    p_len = len(p_list)

    while p_len != 0:
        check = "/".join([p_list[p_len - 1], check])
        if os.path.exists(check):
            result = os.path.join(check, uri)
            return result

        p_len = p_len - 1

    return os.path.abspath(result)

# TODO: Need to fix this! Conversion code is brittle because it only works if LibreOffice is installed. In the short term, we can ignore the issue because nobody's saving in docx any more. In the long term, we should ensure that LibreOffice is somewhere in the provisioning scripts (either on the Gunicorn container or the host) and the conversion part of this script fails gracefully if not.

# TODO: Conversion code cribbed from https://michalzalecki.com/converting-docx-to-pdf-using-python/
def convert(folder, filename, timeout=None):
    args = [
        "libreoffice",
        "--headless",
        "--convert-to",
        "pdf",
        "--outdir",
        folder,
        f"{folder}/{filename}",
    ]

    process = subprocess.run(
        args, stdout=subprocess.PIPE, stderr=subprocess.PIPE, timeout=timeout
    )
    filename = re.search("-> (.*?) using filter", process.stdout.decode())

    if filename is None:
        raise LibreOfficeError(process.stdout.decode())
    else:
        return filename.group(1)


class LibreOfficeError(Exception):
    def __init__(self, output):
        self.output = output


def merge_minutes():
    src = "/mnt/c/Users/stick/Dropbox/CID-Minutes"
    folders = [item.name for item in os.scandir(src) if item.is_dir()]

    for folder in folders:
        merger = (
            PdfFileMerger()
        )  # A new merger for each folder will ensure no 1516-page files.
        dest = os.path.join(storage_path("dropbox/minutes"), f"{folder}.pdf")

        # This drops a merged copy in the Dropbox folder for easy access.
        reflect = os.path.join(src, f"{folder}.pdf")

        def listdir():
            return os.listdir(f"{src}/{folder}")

        # Check for and convert any docx files first.
        for filename in listdir():
            if filename.endswith((".doc", ".docx")):
                convert(f"{src}/{folder}", filename)

        for filename in listdir():
            logger.warn(f"Merging {filename}")
            if filename.endswith(".pdf"):
                merger.append(
                    PdfFileReader(open(os.path.join(f"{src}/{folder}", filename), "rb"))
                )

        merger.write(dest)
        merger.write(reflect)


if __name__ == "__main__":
    # merge_minutes()
    print(os.path.dirname(appname.__file__))
