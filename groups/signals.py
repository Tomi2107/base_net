from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Group, GroupMember
from notifications.utils import create_notification
from friends.models import Friendship
from django.db.models import Q 


@receiver(post_save, sender=Group)
def group_created_notification(sender, instance, created, **kwargs):
    if not created:
        return

    creator = instance.creator

    friendships = Friendship.objects.filter(
        Q(user1=creator) | Q(user2=creator)
    )

    for friendship in friendships:
        friend = friendship.user2 if friendship.user1 == creator else friendship.user1

        create_notification(
            to_user=friend,
            from_user=creator,
            notification_type="group",
            text=f"{creator.username} creó un nuevo grupo: {instance.name}",
            url=f"/groups/?highlight={instance.id}/"
        )



@receiver(post_save, sender=Group)
def create_group_owner(sender, instance, created, **kwargs):
    """
    Al crear un grupo:
    - El creador pasa a ser owner
    - Status aprobado automáticamente
    """
    if not created:
        return

    GroupMember.objects.create(
        group=instance,
        user=instance.creator,
        role="owner",
        status="approved",
    )
