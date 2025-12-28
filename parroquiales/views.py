from django.views.generic import ListView, View
from django.shortcuts import redirect
from django.contrib.auth.mixins import LoginRequiredMixin

from .models import ParroquialPost
from .forms import ParroquialPostForm

from django.db import models


class ParroquialesListView(LoginRequiredMixin, ListView):
    model = ParroquialPost
    template_name = "pages/parroquiales.html"
    context_object_name = "posts"
    paginate_by = 10

    def get_queryset(self):
        qs = ParroquialPost.objects.select_related("author")

        print("🟢 TOTAL POSTS EN DB:", qs.count())

        q = self.request.GET.get("q")
        service = self.request.GET.get("service")

        print("🔎 FILTROS -> q:", q, "| service:", service)

        if q:
            qs = qs.filter(
                models.Q(content__icontains=q) |
                models.Q(zone__icontains=q)
            )
            print("🔵 POSTS TRAS FILTRO TEXTO:", qs.count())

        if service:
            qs = qs.filter(service_type=service)
            print("🟣 POSTS TRAS FILTRO SERVICE:", qs.count())

        final_qs = qs.order_by("-created_at")
        print("✅ POSTS DEVUELTOS AL TEMPLATE:", final_qs.count())

        return final_qs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["form"] = ParroquialPostForm()
        print("📦 CONTEXTO ENVIADO AL TEMPLATE")
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
