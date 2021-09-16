from django import template
from django_jinja import library
import jinja2

# register = template.Library()


# @register.inclusion_tag('nav/site_nav.html')
@library.global_function
@library.render_with('nav/site_nav.html')
def site_nav():
    return {
        'nav_groups': [
            ('About', '#', [
                ('City Market', '/city-market'),
                ('History', '/history'),
                ('Groups', '#', [
                    ('CID', '/cid'),
                    ('Commercial Club', '/commercial-club'),
                    ('Merchants Association', '/merchants'),
                ]),
                ('Loft Living', '/loft-living'),
                ('Parking', '/parking'),
            ]),
            ('Discover', '#', [
                ('Food and Drink', '/food-and-drink'),
                ('Shopping', '/shopping'),
                ('Personal Services', '/personal-services'),
                ('Professional Services', '/professional-services'),
                ('Venues and Events', '/venues-and-events'),
                ('Rentals', '/rentals'),
            ]),
            ('Calendar', '/calendar'),
            ('Newsletter', '/communique'),
        ],
        "scheme": {
            "top": {
                "bg": "blue",
                "text": "gray-100",
            },
            "lv1": {
                "bg": "gray-300",
                "text": "blue",
            },
            "lv2": {
                "bg": "gray-100",
                "text": "blue",
            }
        }
    }

@library.global_function
@library.render_with('nav/site_nav.html')
def hero_nav(cluster_name):
    clusters = {
        'groups': [
            ('CID', '/cid'),
            ('Commercial Club', '/commercial-club'),
            ('Merchants Association', '/merchants'),
        ],
        'directory': [
            ('Food and Drink', '/food-and-drink'),
            ('Shopping', '/shopping'),
            ('Personal Services', '/personal-services'),
            ('Professional Services', '/professional-services'),
            ('Venues and Events', '/venues-and-events'),
            ('Rentals', '/rentals'),
        ]
    }
    return {
        'hero_nav': clusters[cluster_name],
        "scheme": {
            "top": {
                "bg": "green",
                "text": "gray-900",
            }
        }
    }
