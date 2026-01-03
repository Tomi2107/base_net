# pets/views.py
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect,  render
from .models import Pet
from pets.forms import PetForm
from pets.models import Pet

@login_required
def mark_pet_lost(request, pet_id):
    pet = get_object_or_404(
        Pet,
        id=pet_id,
        owner=request.user
    )
    pet.status = 'lost'
    pet.save()
    return redirect('users:edit-profile')


@login_required
def mark_pet_normal(request, pet_id):
    pet = get_object_or_404(
        Pet,
        id=pet_id,
        owner=request.user
    )
    pet.status = 'normal'
    pet.save()
    return redirect('users:edit-profile')

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