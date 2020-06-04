from django.views.generic import ListView
from django.views.generic.base import TemplateView
from tendenci.apps.photos.models import Image, PhotoSet, AlbumCover, License
from tendenci.apps.photos.templatetags.photo_tags import ListPhotosNode, ListPhotoSetsNode

class PhotosetView(ListView):
    template_name = 'photoset.html'
    model = Image

    # def get_queryset(self):
    #     print("Filtering photos.")
    #     self.photoset = get_object_or_404(PhotoSet, guid=self.kwargs['id'])
    #     return Image.objects.filter(photoset=self.photoset)
    
    # def get_context_data(self, *args, **kwargs):
    #     context = super().get_context_data(*args, **kwargs)

    #     # photo_set = get_object_or_404(PhotoSet, id=id)

    #     # context['photos'] = photo_set.get_images(user=None).order_by("position")
    #     # print("Photos added to context")
    #     return context
