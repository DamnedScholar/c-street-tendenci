from django import template

register = template.Library()


@register.inclusion_tag('site_nav.html')
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
            ('Communique', '/communique'),
        ]
    }

@register.inclusion_tag('hero_nav.html')
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
        'hero_nav': clusters[cluster_name]
    }
