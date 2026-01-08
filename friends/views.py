# friends/views.py
from django.views.generic import ListView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from django.contrib.auth import get_user_model
from django.db.models import Q
from django.shortcuts import get_object_or_404, redirect

from django.urls import reverse

from .models import Friendship, FriendRequest

# friends/views.py
from notifications.models import Notification

User = get_user_model()

@login_required
def cancel_request(request, user_id):
    friend_request = get_object_or_404(
        FriendRequest,
        from_user=request.user,
        to_user_id=user_id,
        accepted__isnull=True
    )

    # 🔥 borrar notificación asociada
    Notification.objects.filter(
        from_user=request.user,
        to_user=friend_request.to_user,
        notification_type='friend_request'
    ).delete()

    friend_request.delete()

    return redirect('users:detail', username=friend_request.to_user.username)


@login_required
def remove_friend(request, user_id):
    other_user = get_object_or_404(User, id=user_id)

    # 🔴 borrar amistad (ambas direcciones)
    Friendship.objects.filter(
        user1__in=[request.user, other_user],
        user2__in=[request.user, other_user],
    ).delete()

    # 🔴 borrar cualquier friend request entre ambos
    FriendRequest.objects.filter(
        from_user__in=[request.user, other_user],
        to_user__in=[request.user, other_user],
    ).delete()

    # 🔔 borrar notificaciones de amistad entre ambos
    Notification.objects.filter(
        notification_type='friend_request',
        from_user__in=[request.user, other_user],
        to_user__in=[request.user, other_user],
    ).delete()

    return redirect("users:profile", username=other_user.username)


@login_required
def reject_request(request, request_id):
    fr = get_object_or_404(
        FriendRequest,
        id=request_id,
        to_user=request.user,
        accepted__isnull=True
    )

    fr.delete()

    request.user.notifications.filter(
        url=reverse("friends:requests")
    ).delete()

    return redirect("friends:requests")



@login_required
def accept_request(request, request_id):
    fr = get_object_or_404(
        FriendRequest,
        id=request_id,
        to_user=request.user,
        accepted__isnull=True
    )

    fr.accepted = True
    fr.save()

    Friendship.objects.get_or_create(
        user1=fr.from_user,
        user2=fr.to_user
    )

    # 🔔 eliminar notificación asociada
    request.user.notifications.filter(
        url=reverse("friends:requests")
    ).delete()

    return redirect("friends:requests")


@login_required
def send_friend_request(request, user_id):
    to_user = get_object_or_404(User, id=user_id)

    if to_user != request.user:
        fr, created = FriendRequest.objects.get_or_create(
            from_user=request.user,
            to_user=to_user
        )

        if created:
            Notification.objects.create(
                to_user=to_user,
                from_user=request.user,
                notification_type='friend_request',
                text=f'{request.user.username} te envió una solicitud de amistad',
                url='/friends/requests/'
            )

    return redirect('users:profile', username=to_user.username)




class FriendsListView(LoginRequiredMixin, ListView):
    template_name = 'friends/friends_list.html'
    context_object_name = 'friendships'

    def get_queryset(self):
        return Friendship.objects.filter(
            Q(user1=self.request.user) | Q(user2=self.request.user)
        )

class FriendRequestsView(LoginRequiredMixin, ListView):
    template_name = 'friends/requests.html'
    context_object_name = 'requests'

    def get_queryset(self):
        return FriendRequest.objects.filter(
            to_user=self.request.user,
            accepted__isnull=True
        )

def get_queryset(self):
    self.request.user.notifications.filter(
        notification_type='friend_request',
        is_read=False
    ).update(is_read=True)

    return FriendRequest.objects.filter(
        to_user=self.request.user,
        accepted__isnull=True
    )


