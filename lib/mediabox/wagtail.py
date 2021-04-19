from wagtail.core.models import Collection
from wagtail.images.forms import get_image_form
from wagtail.images.models import Image

from .core import mediabox

ImageForm = get_image_form(Image)

managed_collection = Collection.objects.get_or_create(name="Mediabox")

# Wagtail operations here.
def model_from_path(path):
    path = mediabox.get(query="wedding")
    file = mediabox.open(path)
    form = ImageForm({
        'title': file.basename,
        'file': file.contents,
        'collection': managed_collection
    })

    return form

    # if form.is_valid():
    #     form.save()
