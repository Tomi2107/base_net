from django.views.generic import ListView
from django.db.models import Q
from django.shortcuts import redirect
from django.contrib.auth.decorators import login_required

from .models import Reel
from .forms import ReelForm
from interactions.mixins import SavedByUserMixin  # el mixin genérico
from interactions.models import SavedItem  # solo si necesitás usar SavedItem fuera del mixin


class ReelListView(SavedByUserMixin, ListView):
    model = Reel
    template_name = "pages/reels.html"
    context_object_name = "reels"
    ordering = ["-created_at"]

    # Configuración del mixin
    model_type = Reel
    context_object_name = "reels"

    def get_queryset(self):
        """
        Filtra por búsqueda de texto (q) o servicio (service), si corresponde.
        """
        qs = Reel.objects.select_related("author")
        q = self.request.GET.get("q")
        service = self.request.GET.get("service")

        if q:
            qs = qs.filter(
                Q(caption__icontains=q)  # en Reel se llama caption, no content
            )
    
        return qs.order_by("-created_at")

    def get_context_data(self, **kwargs):
        """
        Agrega el formulario al contexto, el resto lo maneja el mixin.
        """
        context = super().get_context_data(**kwargs)
        context["form"] = ReelForm()
        return context
    
@login_required
def create_reel(request):
    if request.method == "POST":
        form = ReelForm(request.POST, request.FILES)
        if form.is_valid():
            reel = form.save(commit=False)
            reel.author = request.user
            reel.save()
            return redirect("reels:list")

    return redirect("reels:list")
