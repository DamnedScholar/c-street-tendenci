from django import template
from django.shortcuts import get_object_or_404
from django.db.models import Q
from addons.tendenstreet.views.photoset import PhotosetView
from tendenci.apps.photos.models import Image, PhotoSet, AlbumCover, License

register = template.Library()

@register.inclusion_tag('photoset.html', takes_context=True)
def photoset(context, query=""):
    query_spaceless = query.replace(' ','_')

    sets = PhotoSet.objects.filter(     # Look up all matching sets
        Q(name__icontains=query) | Q(tags__icontains=query_spaceless)
    )
    result = Image.objects.filter(      # Look up all matching pictures
        Q(title__icontains=query) | Q(tags__icontains=query_spaceless)
    )

    for s in sets:
        # Grab all images that belong to matching sets and add them to the
        # results set, using the union operation to filter out duplicates.
        s_photos = Image.objects.filter(photoset=s)
        result = result.union(s_photos)

    print(result)
    # print(nofilter)

    # self.photoset = get_object_or_404(PhotoSet, guid=query_id)
    return {
        'photos': result,
        'query': query
    }

    # if query_id == 0:
    #     return "No photoset specified."

    # PhotosetView.as_view(extra_context={'id': query_id})
