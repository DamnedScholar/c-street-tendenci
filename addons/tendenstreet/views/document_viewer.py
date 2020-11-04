from django.views.generic.base import TemplateView


class DocumentViewerView(TemplateView):
    template_name = 'document_viewer.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

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

class WebpackView(DocumentViewerView):
    template_name = 'communique.html'
