import os
import logging; logger = logging.getLogger('Mediabox')
import re

from django.core.files.storage import default_storage

from django.core.files.images import ImageFile
from django.db.models.fields.files import FileField, FieldFile, ImageField, ImageFieldFile

from wagtail.core.models import Collection
from wagtail.documents.forms import get_document_form
from wagtail.documents.models import Document
from wagtail.images.fields import WagtailImageField
from wagtail.images.forms import get_image_form
from wagtail.images.models import Image

from .core import mediabox

DocumentForm = get_document_form(Document)
ImageForm = get_image_form(Image)

managed_collection = Collection.objects.get_or_create(name="Mediabox")[0]

# Wagtail operations here.
def image_from_file(file, path='/', collection=managed_collection):
    # logger.warn(f"Checking path: {path}")
    # file = mediabox.info(path)

    logger.warn(f"Processing file {file} as an image.")
    logger.warn(f"File name: {file.name}")
    logger.warn(f"File path: {path}")

    # img = Image(file=ImageFile(file, name=file.name),
    #     title=file.name, collection=collection)
    img = ImageForm({
        'title': file.name,
        'file': file,
        'collection': collection
    })

    img.clean()

    if img:
        logger.warn(f"We got some errors: {img.errors}")

    img.save()
    
    return img

def document_from_file(file, path='/', collection=managed_collection):
    # logger.warn(f"Checking path: {path}")
    # file = mediabox.info(path)

    logger.warn(f"Processing file {file} as a document.")

    # doc = Document(file=file, title=file.name, collection=collection)

    doc = DocumentForm({
        title: file.name,
        file: file,
        collection: collection
    })

    logger.warn(doc)
    logger.warn(doc.file.name)

    doc.save()

    return doc

def correct_names():
    # TODO: Somehow, documents are getting loaded with their name set to a representation of the file object, not the filename. We can band-aid the problem by using regex to revise all of them.

    for d in Document.objects.all():
        d.title = re.sub("<file \'|\'>", "", d.title)
        d.save()

    for i in Image.objects.all():
        i.title = re.sub("<file \'|\'>", "", i.title)
        i.save()

def collect(paths=None):
    if not paths:
        paths = mediabox.index['photos']

    return [image_from_path(path) for path in paths]

def resolve_collection(name, branch, parent):
    try: coll = parent.get_children().get(name=name)
    except: coll = parent.add_child(name=name)

    if len(branch):
        child = branch.pop(0)

        return resolve_collection(child, branch, coll)
    else:
        return coll

def media_walk():
    logger.warn('Here we go.')
    walker = mediabox.get_walker(config={})
    root = managed_collection

    try:
        child_tree = root.get_descendants()
        logger.warn(f"Trying to purge {len(child_tree)} collections.")
        for coll in child_tree:
            images = [e for e in Image.objects.filter(collection=coll)]
            docs = [e for e in Document.objects.filter(collection=coll)]
            [e.delete() for e in images + docs]
            coll.delete()

        root.numchild = 0
        logger.warn('The managed collection tree has been purged.')
    except Exception as e:
        logger.warn(f'Could not remove child collections. {e}')

        c, i, d = (
            Collection.objects.all(),
            Image.objects.all(),
            Document.objects.all(),
        )

        logger.warn(f"We have {len(c)} collections, {len(i)} images, and {len(d)} documents still hanging around.")
        return False

    for (path, dirs, files) in walker.walk():
        branch = [i for i in f'{path}'.split('/') if i]
        logger.warn(f'Inspecting {branch}')

        if not len(branch):
            coll = root
        else:
            resolved = resolve_collection(branch[0], branch, root)
            coll = resolved.add_child(name=path)

        logger.warn(f"The current collection is {coll}.")

        # new_leaf = resolved.add_child(name=path)
        new_files = []

        for file in files:
            filepath = os.path.join(path, str(file.name))
            try:
                created = image_from_file(file, path=filepath, collection=coll)
            except Exception as e:
                logger.warn(f"Couldn't save this file as an image. Saving as a document instead. Error: {e}")
                created = document_from_file(file, path=filepath, collection=coll)

            new_files.append(created)

        logger.warn(f"Collection {coll} established with contents\n\n{new_files}")

    correct_names()     # This line runs through and fixes the names of files that got added incorrectly until I remedy the bad code.
