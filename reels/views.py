from django.views.generic import ListView
from .models import Reel
from .forms import ReelForm
from django.shortcuts import redirect, render
from django.contrib.auth.decorators import login_required

class ReelListView(ListView):
    model = Reel
    template_name = "pages/reels.html"
    context_object_name = "reels"
    ordering = ["-created_at"]  # para mostrar los más recientes primero

    def get_context_data(self, **kwargs):
        # Obtenemos el contexto base (object_list, etc.)
        context = super().get_context_data(**kwargs)

        # Agregamos el formulario al contexto
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
