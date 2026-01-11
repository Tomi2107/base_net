from friends.utils import get_friendship_status

def friendship_menu(request):
    if not request.user.is_authenticated:
        return {}

    return {
        "friendship_status": None  # default
    }
