from django.views.generic import ListView
from django.shortcuts import redirect
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from interactions.mixins import SavedByUserMixin
from django.db.models import Q

from .models import Group
from .forms import GroupForm


@method_decorator(login_required, name="dispatch")
class GroupListView(ListView, SavedByUserMixin):
    model = Group
    template_name = "pages/groups.html"
    context_object_name = "groups"
    ordering = ["-created_at"]
    model_type = Group
    
    def get_queryset(self):
        """
        Opcional: filtrar por búsqueda de texto o tipo de servicio.
        """
        qs = Group.objects.select_related("creator")
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
        context["form"] = GroupForm()
        return context


@login_required
def create_group(request):
    if request.method == "POST":
        form = GroupForm(request.POST, request.FILES)
        if form.is_valid():
            group = form.save(commit=False)
            group.creator = request.user
            group.save()

    return redirect("groups:list")
