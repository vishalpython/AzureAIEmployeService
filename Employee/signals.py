from django.db.models.signals import post_save
from django.dispatch import receiver
from rest_framework.authtoken.models import Token
from .models import Employee


@receiver(post_save, sender=Employee)
def create_auth_token_for_employee(sender, instance=None, created=None, **kwargs):
    if not created:
        return
    
    if instance.user:
        Token.objects.get_or_create(user=instance.user)

