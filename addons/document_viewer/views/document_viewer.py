import json
from django.views.generic.base import TemplateView


class DocumentViewerView(TemplateView):
    template_name = 'dviewer/document_viewer.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        links = [
                '/proxy/fdff711',
                '/proxy/2cc9611',
                '/proxy/2569311',
            ]

        context = {
            'current': '/proxy/fdff711',
            'links': {
                'as_list': links,
                'as_json': json.dumps(links)
            }
        }

        return context

class CommuniqueView(DocumentViewerView):
    template_name = 'communique.html'
