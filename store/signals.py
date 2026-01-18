from django.db.models.signals import post_save
from django.dispatch import receiver
from django.db.models import Q

from .models import StoreItem
from friends.models import Friendship
from notifications.utils import create_notification


@receiver(post_save, sender=StoreItem)
def store_item_notification(sender, instance, created, **kwargs):
    if not created:
        return

    author = instance.author

    friendships = Friendship.objects.filter(
        Q(user1=author) | Q(user2=author)
    )

    for friendship in friendships:
        friend = friendship.user2 if friendship.user1 == author else friendship.user1

        create_notification(
            to_user=friend,
            from_user=author,
            notification_type="store",
            text=f"{author.username} publicó un nuevo producto/servicio",
            url=f"/store/?highlight={instance.id}/"
        )
