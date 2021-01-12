from django import template

from ..forms import SubscriptionForm

register = template.Library()


@register.inclusion_tag('dviewer/communique.html')
def communique_widget():
    # TODO: Replace mocked content with live API calls.
    context = {
        'current': '/proxy/fdff711',
        'links': [
            '/proxy/fdff711',
            '/proxy/2cc9611',
            '/proxy/2569311',
        ],
        'text': 'Check out our newsletter!'
    }
    
    return context

@register.inclusion_tag('dviewer/subscription.html', takes_context=True)
def subscription_widget():
    return {'form': SubscriptionForm()}
