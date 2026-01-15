from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import FriendRequest
from notifications.utils import create_notification

@receiver(post_save, sender=FriendRequest)
def friend_request_notification(sender, instance, created, **kwargs):
    if created:
        create_notification(
            to_user=instance.to_user,
            from_user=instance.from_user,
            notification_type="friend_request",
            text=f"{instance.from_user.username} te envió una solicitud de amistad",
            url="/friends/requests/"
        )

@receiver(post_save, sender=FriendRequest)
def friend_accept_notification(sender, instance, **kwargs):
    if instance.status == "accepted":
        create_notification(
            to_user=instance.from_user,
            from_user=instance.to_user,
            notification_type="friend_request",
            text=f"{instance.to_user.username} aceptó tu solicitud",
            url=f"/users/{instance.to_user.username}/"
        )
