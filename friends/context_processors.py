from friends.utils import get_friendship_status

def friendship_menu(request):
    if not request.user.is_authenticated:
        return {}

    return {
        "friendship_status": None  # default
    }

def contacts_preview(request):
    if not request.user.is_authenticated:
        return {}

    # amigos aceptados
    friends = (
        request.user.friends
        .filter(accepted=True)
        .select_related("from_user", "to_user")[:6]
    )

    contacts = []
    for fr in friends:
        contact = fr.from_user if fr.to_user == request.user else fr.to_user
        contacts.append(contact)

    return {
        "nav_contacts": contacts
    }
