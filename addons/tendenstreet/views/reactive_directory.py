from django.views.generic.base import TemplateView


class Reactive_DirectoryView(TemplateView):
    template_name = 'reactive_directory.html'

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        context['count'] = 0
        return context
