from django.views.generic import ListView
from django.shortcuts import redirect
from .models import LostFoundPost, LostFoundImage
from .forms import LostFoundForm

class LostFoundFeedView(ListView):
    model = LostFoundPost
    template_name = "pages/lost_found.html"
    context_object_name = "posts"
    paginate_by = 20

    def get_queryset(self):
        qs = LostFoundPost.objects.all().order_by("-created_at")

        # 🔍 FILTROS (GET)
        if self.request.GET.get("status"):
            qs = qs.filter(status=self.request.GET["status"])

        if self.request.GET.get("animal_type"):
            qs = qs.filter(animal_type=self.request.GET["animal_type"])

        if self.request.GET.get("size"):
            qs = qs.filter(size=self.request.GET["size"])

        if self.request.GET.get("color"):
            qs = qs.filter(color__icontains=self.request.GET["color"])

        if self.request.GET.get("pattern"):
            qs = qs.filter(pattern=self.request.GET["pattern"])

        if self.request.GET.get("place"):
            qs = qs.filter(place__icontains=self.request.GET["place"])

        return qs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        # Form en modo búsqueda (GET)
        context["form"] = LostFoundForm(
            self.request.GET or None,
            search_mode=True
        )

        return context

    def post(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return redirect("login")

        form = LostFoundForm(request.POST, request.FILES)

        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user   # 🔥 CAMPO CORRECTO
            post.save()

            for image in request.FILES.getlist("images")[:3]:
                LostFoundImage.objects.create(
                    post=post,
                    image=image
                )
        else:
            print(form.errors)  # 👈 DEBUG REAL

        return redirect("lost_found:feed")

