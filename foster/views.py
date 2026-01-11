from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import ListView
from interactions.mixins import SavedByUserMixin
from django.db.models import Q

from .models import FosterAvailability


class FosterListView(LoginRequiredMixin, SavedByUserMixin, ListView):
    model = FosterAvailability
    template_name = "pages/foster_list.html"
    context_object_name = "fosters"
    model_type = FosterAvailability  # para el mixin
    paginate_by = 10  # opcional

    def get_queryset(self):
        # Solo activos
        qs = FosterAvailability.objects.filter(is_active=True).select_related("user")

        # Búsqueda por username o notas
        q = self.request.GET.get("q")
        if q:
            qs = qs.filter(
                Q(user__username__icontains=q) |
                Q(notes__icontains=q)
            )

        # Filtro opcional por tipo de servicio (si tu modelo tiene service_type)
        service = self.request.GET.get("service")
        if service and hasattr(FosterAvailability, "service_type"):
            qs = qs.filter(service_type=service)

        return qs.order_by("-created_at")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Si necesitas un formulario en el contexto, por ejemplo:
        # context["form"] = FosterForm()
        return context
