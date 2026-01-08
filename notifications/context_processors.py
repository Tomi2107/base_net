# notifications/context_processors.py
def notifications_count(request):
    if request.user.is_authenticated:
        return {
            'notifications_count': request.user.notifications.filter(is_read=False).count()
        }
    return {}
