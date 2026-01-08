from friends.models import FriendRequest, Friendship


def get_friendship_status(user, profile_user):
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
