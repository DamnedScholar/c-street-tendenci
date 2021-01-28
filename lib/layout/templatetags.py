from django_jinja import library
from jinja2 import contextfunction


@contextfunction
@library.global_function
def local_hero(context):
    # Check for a slug passed in the context or delivered from the object being
    # displayed. The top-level context should take priority in the case where
    # there's an object being displayed with a different slug.
    slug = context.slug or context.object.slug

    # TODO: Look for a picture to match this slug. There are some potential performance pitfalls here. I might want to look into caching the hero, but it might also be the case that the pages where I would want to cache this are pages where I want to cache the whole thing, so right now I need to focus on finding a quality image.
    target = slug
    
    return target
