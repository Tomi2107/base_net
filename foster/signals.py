from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import FosterAvailability
from notifications.utils import create_notification
from friends.models import Friendship
from django.db.models import Q


@receiver(post_save, sender=FosterAvailability)
def foster_notification(sender, instance, created, **kwargs):
    if not created:
        return

    author = instance.user

    friendships = Friendship.objects.filter(
        Q(user1=author) | Q(user2=author)
    )

    for f in friendships:
        friend = f.user2 if f.user1 == author else f.user1

        create_notification(
            to_user=friend,
            from_user=author,
            notification_type="post",
            text=f"{author.username} se ofreció para tránsito",
            url=f"/foster/?highlight={instance.id}/"
        )


