from .models import GroupMember


def request_to_join_group(group, user):
    """
    Maneja la lógica de unirse a un grupo
    """
    membership, created = GroupMember.objects.get_or_create(
        group=group,
        user=user,
        defaults={
            "status": "approved" if group.privacy == "public" else "pending",
            "role": "member",
        }
    )

    return membership, created
