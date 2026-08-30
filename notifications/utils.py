from django.core.mail import send_mail
from django.conf import settings
from .models import Notification


def notify(recipient, title, message):
    """
    Creates a real in-app Notification row, and also sends an "email"
    through Django's console backend (prints to your terminal instead
    of a real inbox — safe for demos, no SMTP credentials needed).
    """
    Notification.objects.create(recipient=recipient, title=title, message=message)
    send_mail(
        subject=title,
        message=message,
        from_email=settings.DEFAULT_FROM_EMAIL,
        recipient_list=[recipient.email],
        fail_silently=True,
    )