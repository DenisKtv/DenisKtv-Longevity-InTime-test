from django.core.cache import cache


def check_otp(user_email, otp):
    stored_otp = cache.get(user_email)
    if stored_otp == otp:
        # Отлично, OTP верный!
        return True
    else:
        # Неверный OTP
        return False
