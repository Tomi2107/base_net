from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Message, Conversation
from django.utils import timezone


@receiver(post_save, sender=Message)
def bump_conversation_updated_at(sender, instance, created, **kwargs):
    if not created:
        return

    Conversation.objects.filter(
        id=instance.conversation_id
    ).update(updated_at=timezone.now())
