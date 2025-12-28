from django.views.generic import ListView
from django.shortcuts import redirect
from django.contrib.auth.decorators import login_required
from .models import StoreItem
from .forms import StoreItemForm

class StoreListView(ListView):
    model = StoreItem
    template_name = "pages/store.html"
    context_object_name = "items"
    ordering = ["-created_at"]

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
