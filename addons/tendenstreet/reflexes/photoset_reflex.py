from sockpuppet.reflex import Reflex
from tendenci.apps.photos.models import Image, Pool, PhotoSet
from tendenci.apps.photos.templatetags.photo_tags import ListPhotosNode, ListPhotoSetsNode

class PhotosetReflex(Reflex):
    def resolve(self, *args, **kwargs):
        print("Resolving photos")

        if 'order' not in kwargs:
            kwargs['order'] = '-create_dt'

        self.element.innerHTML = ListPhotosNode('photoset', *args, **kwargs)
        print(ListPhotosNode)

    def increment(self, step=1):
        self.count = int(self.element.dataset['count']) + step
