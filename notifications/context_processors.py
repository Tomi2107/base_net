from .models import Notification

def notifications_nav(request):
    if not request.user.is_authenticated:
        return {}

    notifications = Notification.objects.filter(
        to_user=request.user
    ).order_by("-created_at")

    unread = notifications.filter(is_read=False)

    return {
        # 🔔 contador campana
        "notifications_count": unread.count(),

        # 🔔 dropdown navbar (mezcla, pero resaltamos unread)
        "nav_notifications": notifications[:5],
    }
