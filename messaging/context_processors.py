# messaging/context_processors.py
from django.db.models import Q
from friends.models import FriendRequest
from messaging.models import Conversation, ConversationParticipant

def contacts_list(request):
    if not request.user.is_authenticated:
        return {}

    user = request.user
    contacts = []
    added_ids = set()

    # 1️⃣ Usuarios con conversaciones
    conversations = (
        ConversationParticipant.objects
        .filter(user=user, is_archived=False)
        .select_related("conversation")
        .order_by("-conversation__updated_at")
    )

    for m in conversations:
        other = m.conversation.other_user(user)
        if other and other.id not in added_ids:
            contacts.append(other)
            added_ids.add(other.id)
        if len(contacts) >= 6:
            break

# 2️⃣ Amigos (si todavía hay lugar)
    if len(contacts) < 6:
        friends_qs = FriendRequest.objects.filter(
            accepted=True
        ).filter(
            Q(from_user=user) | Q(to_user=user)
        )

        for f in friends_qs:
            friend = f.to_user if f.from_user == user else f.from_user
            if friend.id not in added_ids:
                contacts.append(friend)
                added_ids.add(friend.id)
            if len(contacts) >= 6:
                break

    return {
        "nav_contacts": contacts
    }

def messages_preview(request):
    if not request.user.is_authenticated:
        return {}

    conversations = (
        Conversation.objects
        .filter(participants=request.user)
        .prefetch_related("participants", "messages")
        .order_by("-updated_at")[:5]
    )

    nav_conversations = []
    for conv in conversations:
        conv.other = conv.other_user(request.user)
        nav_conversations.append(conv)

    return {
        "nav_conversations": nav_conversations
    }
