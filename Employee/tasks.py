from celery import shared_task
from django.utils import timezone
from rest_framework.authtoken.models import Token
from django.conf import settings
from datetime import timedelta

@shared_task
def delete_expired_tokens():
    expiry = getattr(settings, "TOKEN_EXPIRY_TIME", timedelta(hours=24))
    expired_tokens = Token.objects.filter(created__lt=timezone.now() - expiry)
    count = expired_tokens.count()
    expired_tokens.delete()
    return f"Deleted {count} expired tokens."
