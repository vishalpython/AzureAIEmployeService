from django.core.management.base import BaseCommand
from django.utils import timezone
from rest_framework.authtoken.models import Token
from django.conf import settings
from datetime import timedelta

class Command(BaseCommand):
    help = 'Delete Token Based on expiry'

    def handle(self, *args, **options):
        expiry = getattr(settings,'TOKEN_EXPIRY_TIME')

        expired_token = Token.objects.filter(created__lt=timezone.now() - expiry)
        count = expired_token.count()
        expired_token.delete()
        self.stdout.write(self.style.SUCCESS(f"Deleted {count} expired tokens."))