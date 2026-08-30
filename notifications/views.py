from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from .models import Notification


@login_required
def notification_list(request):
    notifications = list(request.user.notifications.all())
    Notification.objects.filter(recipient=request.user, is_read=False).update(is_read=True)
    return render(request, "notifications/list.html", {"notifications": notifications})