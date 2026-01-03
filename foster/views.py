from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import UpdateView, ListView
from django.urls import reverse_lazy

from .models import FosterAvailability

class FosterListView(LoginRequiredMixin, ListView):
    model = FosterAvailability
    template_name = "pages/foster_list.html"
    context_object_name = "fosters"

    def get_queryset(self):
        qs = FosterAvailability.objects.filter(is_active=True)

        q = self.request.GET.get("q")
        if q:
            qs = qs.filter(
                models.Q(user__username__icontains=q) |
                models.Q(notes__icontains=q)
            )

        return qs.select_related("user")
