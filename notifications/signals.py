from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth import get_user_model
from .models import Notification

User = get_user_model()

@receiver(post_save, sender=User)
def welcome_notification(sender, instance, created, **kwargs):
    if created:
        Notification.objects.create(
            to_user=instance,
            notification_type="system",
            text="Bienvenido a la red ",
            url="/"
        )
