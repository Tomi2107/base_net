# notifications/views.py
from django.shortcuts import get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from .models import Notification

@login_required
def go_notification(request, pk):
    notification = get_object_or_404(
        Notification,
        pk=pk,
        to_user=request.user
    )

    notification.is_read = True
    notification.save()

    return redirect(notification.url)
