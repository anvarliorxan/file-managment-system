from itsdangerous import URLSafeTimedSerializer
from django.conf import settings
from django.urls import reverse

def generate_file_share_link(file):
    serializer = URLSafeTimedSerializer(settings.SECRET_KEY)
    token = serializer.dumps({'file_id': file.id})
    download_url = reverse('shared-file-download', kwargs={'token': token})
    return f"{settings.BASE_URL}{download_url}"
