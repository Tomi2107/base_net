from django.db.models.signals import post_save
from django.dispatch import receiver
from django.db.models import Q
from .models import LostFoundPost
from friends.models import Friendship
from notifications.utils import create_notification


@receiver(post_save, sender=LostFoundPost)
def pet_lost_notification(sender, instance, created, **kwargs):
    if not created or instance.status != "lost":
        return

    author = instance.author

    friendships = Friendship.objects.filter(
    Q(user1=instance.author) | Q(user2=instance.author)
)

    for f in friendships:
        friend = f.user2 if f.user1 == instance.author else f.user1

        create_notification(
            to_user=friend,
            from_user=author,
            notification_type="pet",
            text=f"La mascota de {author.username} está perdida 🐾",
            url=f"/lost-found/?highlight={instance.id}/"
        )
