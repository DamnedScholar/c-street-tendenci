from django.views.generic.base import TemplateView

from .document_viewer import CommuniqueView

class ExampleView(CommuniqueView):
    template_name = 'example.html.jinja'
