from django.views.generic import ListView, View
from django.shortcuts import redirect
from django.contrib.auth.mixins import LoginRequiredMixin

from .models import ParroquialPost
from .forms import ParroquialPostForm

from django.db import models
from django.db.models import Q

from interactions.mixins import SavedByUserMixin


class ParroquialesListView(LoginRequiredMixin, SavedByUserMixin, ListView):
    model = ParroquialPost
    template_name = "pages/parroquiales.html"
    context_object_name = "posts"
    paginate_by = 10
    model_type = ParroquialPost  # para mixin

    def get_queryset(self):
        qs = ParroquialPost.objects.select_related("author")

        q = self.request.GET.get("q")
        service = self.request.GET.get("service")

        if q:
            qs = qs.filter(
                models.Q(content__icontains=q) |
                models.Q(zone__icontains=q)
            )

        if service:
            qs = qs.filter(service_type=service)

        return qs.order_by("-created_at")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["form"] = ParroquialPostForm()
        return context


class ParroquialPostCreateView(LoginRequiredMixin, View):
    def post(self, request, *args, **kwargs):

        print("📩 POST DATA RECIBIDO:", request.POST)

        form = ParroquialPostForm(request.POST)

        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.save()

            print("✅ POST GUARDADO:")
            print("   ID:", post.id)
            print("   TITLE:", post.title)
            print("   SERVICE:", post.service_type)
            print("   ZONE:", post.zone)

        else:
            print("❌ FORM ERRORS:")
            print(form.errors)

        return redirect("parroquiales:list")
