from django.utils import timezone
from .models import Ad

def get_ads_for_user(user):
    today = timezone.now().date()

    qs = Ad.objects.filter(
        active=True,
        approved=True,
    )

    if user.is_authenticated:
        zone = getattr(user.profile, "zone", None)
        if zone:
            qs = qs.filter(zones=zone)

    return qs.distinct()
