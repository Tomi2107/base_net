from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import ParroquialPost
from notifications.utils import create_notification

@receiver(post_save, sender=ParroquialPost)
def friend_posted_notification(sender, instance, created, **kwargs):
    if not created:
        return

    author = instance.author

    for friend in author.friends.all():
        create_notification(
            to_user=friend,
            from_user=author,
            notification_type="post",
            text=f"{author.username} nuevos parroquiales",
            url=f"/lost-found/{instance.id}/"
        )
