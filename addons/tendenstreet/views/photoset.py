from django.views.generic.base import TemplateView

class PhotosetView(TemplateView):
    template_name = 'photoset.html'

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        context['photos'] = []
        return context
