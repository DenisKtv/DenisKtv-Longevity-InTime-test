import random
from datetime import timedelta
from celery import shared_task
from django.core.cache import cache
from django.core.mail import send_mail


@shared_task
def send_otp_email(user_email):
    otp_code = ''.join(
        random.choices(
            '0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz',
            k=6
        )
    )

    # Сохранение OTP в Redis с истечением срока действия 10 минут
    cache.set(user_email, otp_code, timeout=timedelta(minutes=3).seconds)

    # Отправка OTP пользователю
    send_mail(
        'Your OTP code',
        f'Your OTP code is {otp_code}',
        'fisherjournalby@gmail.com',
        [user_email],
        fail_silently=False,
    )
