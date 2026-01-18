from django.db.models import Q
from django.contrib.auth import get_user_model

from .models import FriendRequest, Friendship

User = get_user_model()


def get_friendship_status(user, profile_user):
    """
    Devuelve el estado de la relación entre user y profile_user.
    """

    if not user.is_authenticated:
        return "anonymous"

    if user == profile_user:
        return "self"

    # 🤝 ya son amigos (en cualquier orden)
    if Friendship.objects.filter(
        user1__in=[user, profile_user],
        user2__in=[user, profile_user],
    ).exists():
        return "friends"

    # ⏳ solicitud enviada
    if FriendRequest.objects.filter(
        from_user=user,
        to_user=profile_user,
        accepted__isnull=True
    ).exists():
        return "sent"

    # 📩 solicitud recibida
    if FriendRequest.objects.filter(
        from_user=profile_user,
        to_user=user,
        accepted__isnull=True
    ).exists():
        return "received"

    return "none"


def get_friends(user):
    """
    Devuelve una lista de usuarios amigos del user.
    """

    friendships = Friendship.objects.filter(
        Q(user1=user) | Q(user2=user)
    ).select_related("user1", "user2")

    friends = []

    for friendship in friendships:
        if friendship.user1 == user:
            friends.append(friendship.user2)
        else:
            friends.append(friendship.user1)

    return friends


def get_friends_qs(user):
    """
    Devuelve un QuerySet de usuarios amigos (útil para feeds, filtros, paginación).
    """

    friendships = Friendship.objects.filter(
        Q(user1=user) | Q(user2=user)
    )

    friend_ids = [
        f.user2_id if f.user1_id == user.id else f.user1_id
        for f in friendships
    ]

    return User.objects.filter(id__in=friend_ids)
