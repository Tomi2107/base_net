# interactions/views.py
from django.shortcuts import get_object_or_404, redirect, render
from django.contrib.auth.decorators import login_required
from django.contrib.contenttypes.models import ContentType
from django.apps import apps

from .models import SavedItem

# -----------------------------
# Guardar cualquier post
# -----------------------------
@login_required
def save_item(request, model_name, item_id):
    """
    model_name: 'app_label.ModelName', ej: 'reels.Reel'
    """
    model = apps.get_model(*model_name.split('.'))
    item = get_object_or_404(model, id=item_id)

    ct = ContentType.objects.get_for_model(model)
    SavedItem.objects.get_or_create(
        user=request.user,
        content_type=ct,
        object_id=item.id
    )
    return redirect(request.META.get("HTTP_REFERER", "/"))

# -----------------------------
# Quitar de guardados
# -----------------------------
@login_required
def unsave_item(request, model_name, item_id):
    model = apps.get_model(*model_name.split('.'))
    item = get_object_or_404(model, id=item_id)

    ct = ContentType.objects.get_for_model(model)
    SavedItem.objects.filter(
        user=request.user,
        content_type=ct,
        object_id=item.id
    ).delete()

    return redirect(request.META.get("HTTP_REFERER", "/"))

# -----------------------------
# Eliminar StoreItem (solo store)
# -----------------------------
from store.models import StoreItem

@login_required
def remove_store_item(request, item_id):
    item = get_object_or_404(StoreItem, id=item_id, owner=request.user)
    item.delete()
    return redirect("store:list")

# -----------------------------
# Lista de items guardados
# -----------------------------
def saved_items_list(request):
    saved_items = (
        SavedItem.objects
        .filter(user=request.user)
        .select_related("content_type")
    )

    items = []

    for s in saved_items:
        obj = s.content_object
        if not obj:
            continue

        items.append({
            "object": obj,
            "model": s.content_type.model,          # "group", "lostfoundpost", etc.
            "app": s.content_type.app_label,        # opcional
            "is_saved": True,
        })

    return render(
        request,
        "interactions/saved_items_list.html",
        {"items": items}
    )
