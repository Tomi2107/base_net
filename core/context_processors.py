# core/context_processors.py
from pets.models import Pet

def user_pets(request):
    if request.user.is_authenticated:
        return {'pets': Pet.objects.filter(owner=request.user)}
    return {'pets': []}
