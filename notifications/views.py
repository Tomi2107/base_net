from django.shortcuts import get_object_or_404, redirect, render
from django.contrib.auth.decorators import login_required
from .models import Notification

@login_required
def go_notification(request, pk):
    notification = get_object_or_404(
        Notification,
        pk=pk,
        to_user=request.user
    )

    # marcar como leída
    if not notification.is_read:
        notification.is_read = True
        notification.save(update_fields=["is_read"])

    return redirect(notification.url)

@login_required
def notifications_list(request):
    notifications = (
        Notification.objects
        .filter(to_user=request.user)
        .order_by("-created_at")
    )

    return render(request, "notifications/list.html", {
        "notifications": notifications
    })
