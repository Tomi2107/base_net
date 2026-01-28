# search/views.py
from django.views.generic import TemplateView
from .services import global_search


class GlobalSearchView(TemplateView):
    template_name = "search/results.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        query = self.request.GET.get("q", "").strip()

        context["query"] = query

        if query:
            context.update(global_search(query))
        else:
            # siempre definir claves para que el template no rompa
            context.update({
                "profiles": [],
                "opinions": [],
                "reels": [],
                "groups": [],
                "pets": [],
                "ads": [],
                "fosters": [],
                "parroquiales":[],
                "store": [],
            })

        return context
