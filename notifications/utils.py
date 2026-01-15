from .models import Notification

def create_notification(
    *,
    to_user,
    from_user=None,
    notification_type,
    text,
    url=""
):
    if to_user == from_user:
        return  # 🔕 no notificarse a uno mismo

    Notification.objects.create(
        to_user=to_user,
        from_user=from_user,
        notification_type=notification_type,
        text=text,
        url=url
    )
