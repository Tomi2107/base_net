from django.views.generic import ListView
from django.shortcuts import redirect
from django.contrib.auth.decorators import login_required
from .models import StoreItem
from .forms import StoreItemForm
from interactions.mixins import SavedByUserMixin
from django.db.models import Q

class StoreListView( SavedByUserMixin, ListView):
    model = StoreItem
    template_name = "pages/store.html"
    context_object_name = "items"
    ordering = ["-created_at"]
    model_type = StoreItem
    paginate_by = 12
    
    def get_queryset(self):
        """
        Opcional: filtrar por búsqueda de texto o tipo de servicio.
        """
        qs = StoreItem.objects.select_related("author")
        q = self.request.GET.get("q")
        service = self.request.GET.get("service")

        if q:
            qs = qs.filter(
                Q(content__icontains=q) |
                Q(zone__icontains=q)
            )
        if service:
            qs = qs.filter(service_type=service)

        return qs.order_by("-created_at")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["form"] = StoreItemForm()
        return context


@login_required
def create_item(request):
    if request.method == "POST":
        form = StoreItemForm(request.POST, request.FILES)
        if form.is_valid():
            item = form.save(commit=False)
            item.author = request.user
            item.save()
    return redirect("store:list")
