# messaging/services.py
def mark_conversation_as_read(conversation, user):
    ConversationParticipant.objects.filter(
        conversation=conversation,
        user=user
    ).update(unread_count=0)

    conversation.messages.filter(
        is_read=False
    ).exclude(sender=user).update(is_read=True)
