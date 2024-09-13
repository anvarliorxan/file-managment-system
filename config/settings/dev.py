from config.settings.com import *

DEBUG = True

ALLOWED_HOSTS = ['*']


"""
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}
"""


DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': env('POSTGRES_DB', default='mydatabase'),
        'USER': env('POSTGRES_USER', default='myuser'),
        'PASSWORD': env('POSTGRES_PASSWORD', default='mypassword'),
        'HOST': env('POSTGRES_HOST', default='db'),
        'PORT': env('POSTGRES_PORT', default='5432')
    }
}



BASE_URL = 'http://127.0.0.1:8000'


STATICFILES_DIRS = [
    BASE_DIR / 'static/ssr'
]