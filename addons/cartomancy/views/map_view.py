from django.views.generic.base import TemplateView


class MapViewView(TemplateView):
    template_name = 'map_view.html'

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        context['count'] = 0
        return context
