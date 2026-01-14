from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from lost_found.models import LostFoundPost
from lost_found.forms import LostFoundForm
from pets.models import Pet
from interactions.models import SavedItem
from django.contrib.contenttypes.models import ContentType
from interactions.utils import enrich_items_with_save_state


@login_required
def lost_found_feed(request):
    posts = LostFoundPost.objects.all().order_by("-created")

    # 🔍 SEARCH FORM (GET)
    search_form = LostFoundForm(request.GET or None, search_mode=True)
    if request.method == "GET" and search_form.is_valid():
        data = search_form.cleaned_data

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

    # ➕ CREATE FORM (POST)
    create_form = LostFoundForm()
    if request.method == "POST":
        create_form = LostFoundForm(request.POST, request.FILES)
        if create_form.is_valid():
            post = create_form.save(commit=False)
            post.author = request.user
            post.save()

            for img in request.FILES.getlist("images")[:3]:
                post.images.create(image=img)

            return redirect("lost_found:feed")

    # ⭐ Guardados
    posts = enrich_items_with_save_state(posts, request.user)

    return render(request, "pages/lost_found.html", {
        "search_form": search_form,
        "create_form": create_form,
        "posts": posts,
    })


@login_required
def remove_lost_post(request, pet_id):
    pet = get_object_or_404(
        Pet,
        id=pet_id,
        owner=request.user
    )

    # borrar SOLO el último post "lost" del usuario
    post = (
        LostFoundPost.objects
        .filter(author=request.user, status="lost")
        .order_by("-created")
        .first()
    )

    if post:
        post.delete()

    pet.status = "normal"
    pet.save()

    return redirect("home")




