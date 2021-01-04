import logging
import json

from django.http import HttpResponse
from django.template.response import TemplateResponse
from django.shortcuts import render
from django.views.generic.base import TemplateView

from ..forms import SubscriptionForm

class DocumentViewerView(TemplateView):
    template_name = 'dviewer/document_viewer.html'

class CommuniqueView(DocumentViewerView):
    template_name = 'communique.html'
    links = [
        '/proxy/fdff711',
        '/proxy/2cc9611',
        '/proxy/2569311',
    ]
    extra_context = {
        'current': '/proxy/fdff711',
        'links': {
            'as_list': links,
            'as_json': json.dumps(links)
        },
        'form': SubscriptionForm(auto_id=True)
    }

    # def get(self, request, *args, **kwargs):
    #     context = self.get_context_data(**kwargs)

    #     return render(request, self.template_name, context)
