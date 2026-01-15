from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Group
from notifications.utils import create_notification

@receiver(post_save, sender=Group)
def friend_posted_notification(sender, instance, created, **kwargs):
    if not created:
        return

    author = instance.author

    for friend in author.friends.all():
        create_notification(
            to_user=friend,
            from_user=author,
            notification_type="post",
            text=f"{author.username} publicó un nuevo grupo",
            url=f"/lost-found/{instance.id}/"
        )
