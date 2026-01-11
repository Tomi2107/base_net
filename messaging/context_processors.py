from .models import Conversation
from django.db.models import Prefetch

def messages_preview(request):
    if not request.user.is_authenticated:
        return {}

    conversations = (
        Conversation.objects
        .filter(participants=request.user)
        .prefetch_related("participants", "messages")
        .order_by("-updated_at")[:5]
    )

    return {
        "nav_conversations": conversations
    }
