# messaging/utils.py
from .models import Conversation
from django.db.models import Q


def get_or_create_conversation(user1, user2):
    conversation = Conversation.objects.filter(
        participants=user1
    ).filter(
        participants=user2
    ).first()

    if conversation:
        return conversation

    conversation = Conversation.objects.create()
    conversation.participants.add(user1, user2)
    return conversation
