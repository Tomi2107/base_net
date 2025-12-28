# pets/views.py
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect
from .models import Pet

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
