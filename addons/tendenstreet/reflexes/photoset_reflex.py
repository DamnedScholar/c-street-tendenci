from sockpuppet.reflex import Reflex
from tendenci.apps.photos.models import Image, PhotoSet, AlbumCover, License
from tendenci.apps.photos.templatetags.photo_tags import ListPhotosNode, ListPhotoSetsNode


class PhotosetReflex(Reflex):
    def resolve(self, *args, **kwargs):
        print("Resolving photos")

        photo_set = get_object_or_404(PhotoSet, id=id)

        # if 'order' not in kwargs:
        #     kwargs['order'] = '-create_dt'
        #
        # self.element.innerHTML = ListPhotosNode('photoset', *args, **kwargs)
        # print(ListPhotosNode)

    def increment(self, step=1):
        self.count = int(self.element.dataset['count']) + step
