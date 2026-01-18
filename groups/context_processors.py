from .models import Group, GroupMember

def groups_sidebar(request):
    if not request.user.is_authenticated:
        return {}

    my_groups = Group.objects.filter(
        memberships__user=request.user,
        memberships__status="approved"
    ).distinct()

    # si todavía no usás follow, dejalo vacío
    followed_groups = []

    return {
        "my_groups": my_groups[:5],
        "followed_groups": followed_groups[:5],
    }

