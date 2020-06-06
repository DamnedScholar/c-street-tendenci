from django.db.models import Q
from tendenci.apps.photos.models import Image, PhotoSet, AlbumCover, License

def get_images_for_entry(query):
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

    return result