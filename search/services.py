# search/services.py
from django.db.models import Q
from accounts.models import Profile

def global_search(query):
    profiles = Profile.objects.filter(
        Q(user__username__icontains=query) |
        Q(user__first_name__icontains=query) |
        Q(user__last_name__icontains=query) |
        Q(bio__icontains=query) |
        Q(location__icontains=query)
    ).select_related("user")

    return {
        "profiles": profiles
    }
