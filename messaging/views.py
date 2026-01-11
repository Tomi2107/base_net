# messaging/views.py
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth import get_user_model
from .models import Conversation, Message
from .utils import get_or_create_conversation
from django.db.models import Prefetch, Count, Q

from messaging.models import Conversation, Message, ConversationParticipant


User = get_user_model()


@login_required
def start_conversation(request, username):
    other_user = get_object_or_404(User, username=username)
    conversation = get_or_create_conversation(request.user, other_user)
    return redirect("messaging:conversation_detail", pk=conversation.pk)

@login_required
def conversation_detail(request, pk):

    conversation = get_object_or_404(
        Conversation.objects.prefetch_related("messages", "participants"),
        pk=pk,
        participants=request.user
    )

    # POST: enviar mensaje
    if request.method == "POST":
        Message.objects.create(
            conversation=conversation,
            sender=request.user,
            body=request.POST.get("body")
        )

        # sumar unread al otro
        other = conversation.other_user(request.user)
        member = ConversationParticipant.objects.get(
            conversation=conversation,
            user=other
        )
        member.unread_count += 1
        member.save()

        return redirect("messaging:conversation_detail", pk=pk)

    # SIDEBAR CHAT (preparado)
    sidebar_conversations = []

    memberships = (
        ConversationParticipant.objects
        .filter(user=request.user, is_archived=False)
        .select_related("conversation")
        .prefetch_related("conversation__messages", "conversation__participants")
    )

    for m in memberships:
        conv = m.conversation
        sidebar_conversations.append({
            "id": conv.id,
            "other": conv.other_user(request.user),
            "last_message": conv.last_message(),
            "unread_count": m.unread_count,
        })

    # marcar conversación actual como leída
    ConversationParticipant.objects.filter(
        conversation=conversation,
        user=request.user
    ).update(unread_count=0)

    return render(
        request,
        "components/messages/conversation_detail.html",
        {
            "conversation": conversation,
            "sidebar_conversations": sidebar_conversations,
            "other_user": conversation.other_user(request.user),
        }
    )


    
@login_required
def inbox(request):
    conversations = (
        Conversation.objects
        .filter(participants=request.user)
        .prefetch_related(
            Prefetch(
                "messages",
                queryset=Message.objects.order_by("-created_at")
            ),
            "participants",
            "memberships"
        )
        .order_by("-updated_at")
    )

    data = []
    for conv in conversations:
        other = conv.participants.exclude(id=request.user.id).first()
        membership = conv.memberships.get(user=request.user)
        last_message = conv.messages.first()

        data.append({
            "conversation": conv,
            "other_user": other,
            "last_message": last_message,
            "unread_count": membership.unread_count,
        })

    return render(request, "components/messages/inbox.html", {
        "conversations": data
    })


def navbar_conversations(request):
    conversations = (
        Conversation.objects
        .filter(participants=request.user)
        .prefetch_related("participants", "messages")
        .order_by("-updated_at")[:10]
    )

    nav_conversations = []
    for conv in conversations:
        conv.other = conv.other_user(request.user)
        nav_conversations.append(conv)

    return {
        "nav_conversations": nav_conversations
    }
    

@login_required
def archive_conversation(request, pk):
    membership = get_object_or_404(
        ConversationParticipant,
        conversation_id=pk,
        user=request.user
    )

    membership.is_archived = True
    membership.save()

    return redirect("messaging:inbox")

@login_required
def delete_conversation(request, pk):
    membership = get_object_or_404(
        ConversationParticipant,
        conversation_id=pk,
        user=request.user
    )

    membership.delete()

    return redirect("messaging:inbox")

@login_required
def archived_inbox(request):
    memberships = (
        ConversationParticipant.objects
        .filter(user=request.user, is_archived=True)
        .select_related("conversation")
        .prefetch_related("conversation__messages", "conversation__participants")
    )

    data = []
    for m in memberships:
        conv = m.conversation
        data.append({
            "conversation": conv,
            "other_user": conv.other_user(request.user),
            "last_message": conv.last_message(),
            "unread_count": m.unread_count,
        })

    return render(
        request,
        "components/messages/archived_inbox.html",
        {
            "conversations": data
        }
    )

@login_required
def unarchive_conversation(request, pk):
    membership = get_object_or_404(
        ConversationParticipant,
        conversation_id=pk,
        user=request.user
    )

    membership.is_archived = False
    membership.save()

    return redirect("messaging:archived_inbox")
