from django.core.cache import cache
from rest_framework_simplejwt.tokens import RefreshToken


def get_token_for_user(user):
    refresh = RefreshToken.for_user(user)
    return str(refresh.access_token)


def check_otp(user_email, otp):
    stored_otp = cache.get(user_email)
    if stored_otp == otp:
        return True
    else:
        return False
