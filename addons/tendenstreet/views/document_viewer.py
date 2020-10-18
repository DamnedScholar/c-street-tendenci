from django.views.generic.base import TemplateView


class DocumentViewerView(TemplateView):
    template_name = 'document_viewer.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context = {
            'current': 'https://madmimi.com/p/2569311',
            'links': [
                'https://madmimi.com/p/2569311',
                'https://madmimi.com/p/2569311',
                'https://madmimi.com/p/2569311'
            ],
            'text': 'Check out our newsletter!'
        }

        return context
