from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from .models import LostFoundPost
from .forms import LostFoundForm
from pets.models import Pet

def feed(request):
    posts = LostFoundPost.objects.all().order_by("-created")

    # ---------- SEARCH (GET) ----------
    if request.method == "GET":
        form = LostFoundForm(
            request.GET or None,
            search_mode=True
        )

        if form.is_valid():
            data = form.cleaned_data

            if data.get("status"):
                posts = posts.filter(status=data["status"])
            if data.get("animal_type"):
                posts = posts.filter(animal_type=data["animal_type"])
            if data.get("size"):
                posts = posts.filter(size=data["size"])
            if data.get("color"):
                posts = posts.filter(color__icontains=data["color"])
            if data.get("pattern"):
                posts = posts.filter(pattern=data["pattern"])
            if data.get("place"):
                posts = posts.filter(place__icontains=data["place"])

    # ---------- CREATE (POST) ----------
    else:
        form = LostFoundForm(request.POST, request.FILES)

        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.save()

            for img in request.FILES.getlist("images")[:3]:
                post.images.create(image=img)

            return redirect("lost_found:feed")

    return render(request, "pages/lost_found.html", {
        "form": form,
        "posts": posts
    })

@login_required
def remove_lost_post(request, pet_id):
    pet = get_object_or_404(
        Pet,
        id=pet_id,
        owner=request.user
    )

    # borrar el post de lost_found del usuario
    LostFoundPost.objects.filter(
        author=request.user,
        status="lost"
    ).delete()

    # devolver mascota a normal
    pet.status = "normal"
    pet.save()

    return redirect("home")