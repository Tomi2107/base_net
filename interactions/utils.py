from django.contrib.contenttypes.models import ContentType
from .models import SavedItem


def enrich_items_with_save_state(items, user):
    items = list(items)

    if not items:
        return items

    model = items[0].__class__
    ct = ContentType.objects.get_for_model(model)

    saved_ids = set()
    if user.is_authenticated:
        saved_ids = set(
            SavedItem.objects.filter(
                user=user,
                content_type=ct,
                object_id__in=[item.id for item in items]
            ).values_list("object_id", flat=True)
        )

    model_name = f"{model._meta.app_label}.{model._meta.model_name}"

    for item in items:
        # 🔐 dueño universal
        owner = (
            getattr(item, "owner", None)
            or getattr(item, "creator", None)
            or getattr(item, "author", None)
            or getattr(item, "user", None)
        )
        item.is_owner = owner == user

        # ⭐ guardado
        item.is_saved_by_user = item.id in saved_ids

        # 🔗 url save/unsave
        item.model_name = model_name

    return items
