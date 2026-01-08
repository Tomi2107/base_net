def user_pets(request):
    if request.user.is_authenticated:
        return {
            'pets': request.user.pets.all()
        }
    return {
        'pets': []
    }
