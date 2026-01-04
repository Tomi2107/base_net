# pets/views.py
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect,  render
from .models import Pet
from pets.forms import PetForm
from pets.models import Pet
from lost_found.models import LostFoundPost

SIZE_MAP = {
    "xs": "xs",
    "s": "s",
    "m": "m",
    "l": "l",
    "xl": "xl",

    # por si Pet usa textos largos
    "small": "s",
    "medium": "m",
    "large": "l",
    "extra_large": "xl",
}

@login_required
def mark_pet_lost(request, pet_id):
    pet = get_object_or_404(
        Pet,
        id=pet_id,
        owner=request.user
    )

    pet.status = "lost"
    pet.save()

    LostFoundPost.objects.create(
        author=request.user,
        status="lost",

        animal_type=pet.species,
        animal_other=pet.breed if pet.species == "other" else "",

        size=SIZE_MAP.get(pet.size, "m"),  # ✅ FIX CLAVE
        color=pet.color,

        pattern="liso",
        place=(
            request.user.profile.location
            if hasattr(request.user, "profile") and request.user.profile.location
            else "No especificado"
        ),

        description=(
            f"Se perdió {pet.name}. "
            f"Raza: {pet.breed or 'No especificada'}. "
            f"{pet.notes or ''}"
        )
    )

    return redirect("lost_found:feed")



@login_required
def mark_pet_normal(request, pet_id):
    pet = get_object_or_404(
        Pet,
        id=pet_id,
        owner=request.user
    )
    pet.status = 'normal'
    pet.save()
    return redirect('home')

@login_required
def mark_pet_dating(request, pet_id):
    pet = get_object_or_404(
        Pet,
        id=pet_id,
        owner=request.user
    )
    pet.status = 'dating'
    pet.save()
    return redirect('home')


@login_required
def edit_pet(request, pk):
    pet = get_object_or_404(Pet, pk=pk, owner=request.user)

    if request.method == "POST":
        form = PetForm(request.POST, instance=pet)
        if form.is_valid():
            form.save()
            return redirect("users:edit-profile")
    else:
        form = PetForm(instance=pet)

    return render(request, "users/pet_edit.html", {
        "form": form,
        "pet": pet
    })

@login_required
def delete_pet(request, pk):
    pet = get_object_or_404(Pet, pk=pk, owner=request.user)

    if request.method == "POST":
        pet.delete()
        return redirect("users:edit-profile")

    return render(request, "users/pet_delete.html", {
        "pet": pet
    })