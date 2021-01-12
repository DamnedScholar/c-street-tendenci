from django.views.generic.base import TemplateView


class NcisView(TemplateView):
    template_name = 'ncis.html.jinja'

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        context['count'] = 0
        return context
