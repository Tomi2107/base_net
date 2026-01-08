# search/views.py
from django.views.generic import TemplateView
from .services import global_search

class GlobalSearchView(TemplateView):
    template_name = 'search/results.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        query = self.request.GET.get('q', '').strip()

        if query:
            results = global_search(query)
        else:
            results = {}

        context.update(results)
        context['query'] = query

        return context
