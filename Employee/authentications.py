from datetime import timedelta
from django.conf import settings
from django.utils import timezone
from rest_framework.authentication import TokenAuthentication
from rest_framework.exceptions import AuthenticationFailed


class ExpiringAuthentication(TokenAuthentication):

    def authenticate_credentials(self, key):
        user , token = super().authenticate_credentials(key)

        expiry = getattr(settings,"TOKEN_EXPIRY_TIME",timedelta(minutes=1))

        if token.created < timezone.now() - expiry:
            raise AuthenticationFailed("Token expriy please login again")
        return (user,token)