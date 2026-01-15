from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import LostFoundPost
from notifications.utils import create_notification


@receiver(post_save, sender=LostFoundPost)
def pet_lost_notification(sender, instance, created, **kwargs):
    if created and instance.status == "lost":
        for friend in instance.author.friends.all():
            create_notification(
                to_user=friend,
                from_user=instance.author,
                notification_type="pet",
                text=f"Firu de {instance.author.username} s perdido 🐾",
                url=f"/lost-found/{instance.id}/"
            )
            

