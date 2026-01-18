from django.db.models.signals import post_save
from django.dispatch import receiver
from django.db.models import Q

from .models import ParroquialPost
from friends.models import Friendship
from notifications.utils import create_notification


@receiver(post_save, sender=ParroquialPost)
def parroquial_post_notification(sender, instance, created, **kwargs):
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
            notification_type="parroquial",
            text=f"{author.username} publicó un aviso en {instance.zone}",
            url=f"/parroquiales/?highlight={instance.id}/"
        )
