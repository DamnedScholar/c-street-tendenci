from django_jinja import library
from jinja2 import contextfunction


@contextfunction
@library.global_function
@library.render_with('hammer.jinja.html')
def reflex_hammer():
    # Create a free-floating web component (so its styles and internals are encapsulated in shadow DOM) with internal content that contains two log flows. One log will be built in JS and controlled by the Stimulus controller. The other will be tied to a resource on the server via a URL endpoint and rerender based on changes in the resource. When used in conjunction with `django-sockpuppet`, the `reflex-hammer` will be able to display messages from the client and server in parallel.
    return {}
