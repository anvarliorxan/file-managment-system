from __future__ import absolute_import, unicode_literals
from celery import shared_task
from datetime import datetime, timedelta, timezone
import secrets
from django.core.cache import caches
from apps.user.models import User
from apps.core.utils import SoftlineSms
import threading
from apps.user.models import File


@shared_task
def send_otp_to_number(phone):
    if User.objects.filter(phone=phone).exists():
        # generate 4-digit OTP
        otp = str(secrets.randbelow(10**4)).zfill(4)

        # set OTP expiration time to 100 seconds
        expiration_time = datetime.now(
            timezone.utc) + timedelta(seconds=int(180))

        otp_cache = caches['otp-cache']

        # cache OTP and expiration time
        otp_cache.set(
            otp,
            (phone, expiration_time),
            timeout=int(180)
        )
        # send OTP to user's phone

        text = f'{otp} - Sizin OTP kodunuz. Xahiş olunur, birdəfəlik kodu digər şəxslərlə paylaşmayasınız'
        sms = SoftlineSms()
        sms.send(phone=phone, text=text)
        return True
    return False


@shared_task
def remove_file(id):
    def thread_function():
        file = File.objects.filter(id=id).first()
        scheduled_task = file.scheduled_task.first()
        file.delete()
        scheduled_task.status = 'completed'
        scheduled_task.save()

    threading.Thread(target=thread_function).start()