from django.db.models import Q

from accounts.models import Profile, UserOpinion
from groups.models import Group
from pets.models import Pet
from ads.models import Ad
from foster.models import FosterAvailability
from reels.models import Reel
from store.models import StoreItem
from parroquiales.models import ParroquialPost


def global_search(query):
    profiles = Profile.objects.filter(
        Q(user__username__icontains=query) |
        Q(user__first_name__icontains=query) |
        Q(user__last_name__icontains=query) |
        Q(bio__icontains=query) |
        Q(location__icontains=query)
    ).select_related("user").distinct()

    opinions = UserOpinion.objects.filter(
    profile__isnull=False
    ).filter(
        Q(comment__icontains=query)
    ).select_related("author", "profile").order_by("-created").distinct()


    reels = Reel.objects.filter(
        Q(caption__icontains=query),
    ).select_related("author").order_by("-created_at")[:20]

    groups = Group.objects.filter(
        Q(name__icontains=query) |
        Q(description__icontains=query)
    )

    pets = Pet.objects.filter(
        Q(name__icontains=query) |
        Q(breed__icontains=query)
    )

    ads = Ad.objects.filter(
        approved=True,
        active=True,
        title__icontains=query
    )

    fosters = FosterAvailability.objects.filter(
        is_active=True
    ).filter(
        Q(notes__icontains=query) |
        Q(animal_other__icontains=query) |
        Q(animal_type__icontains=query) |
        Q(health_condition__icontains=query) |
        Q(user__username__icontains=query)
    ).select_related("user")
    
    parroquiales = ParroquialPost.objects.filter(
        Q(title__icontains=query) |
        Q(service_type__icontains=query) |
        Q(zone__icontains=query) |
        Q(content__icontains=query) |
        Q(author__username__icontains=query) |
        Q(author__first_name__icontains=query) |
        Q(author__last_name__icontains=query)
    ).select_related("author").distinct()

    
    store = StoreItem.objects.filter(
        Q(title__icontains=query) |
        Q(description__icontains=query) |
        Q(item_type__icontains=query) |
        Q(location__icontains=query) |
        Q(author__username__icontains=query) |
        Q(author__first_name__icontains=query) |
        Q(author__last_name__icontains=query)
    ).select_related("author").distinct()



    return {
        "profiles": profiles,
        "opinions": opinions,
        "reels": reels,
        "groups": groups,
        "pets": pets,
        "ads": ads,
        "fosters": fosters,
        "parroquiales_items": parroquiales,
        "store_items": store,
        
    }
