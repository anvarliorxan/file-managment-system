from config.settings.com import *
import sentry_sdk

DEBUG = False

ALLOWED_HOSTS = ['*']


DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': env('POSTGRE_NAME', default=""),
        'USER': env('POSTGRE_USER', default=""),
        'PASSWORD': env('POSTGRE_PASS', default=""),
        'HOST': env('POSTGRE_HOST', default=""),
        'PORT': env('POSTGRE_PORT', default="5432"),
    }
}

BASE_URL = 'https://b2club.az'
STATIC_ROOT = BASE_DIR / 'static'


sentry_sdk.init(
    dsn="https://9639c8957289e06523efd41f3639a501@o4506960749264896.ingest.us.sentry.io/4506960864018432",
    # Set traces_sample_rate to 1.0 to capture 100%
    # of transactions for performance monitoring.
    traces_sample_rate=1.0,
    # Set profiles_sample_rate to 1.0 to profile 100%
    # of sampled transactions.
    # We recommend adjusting this value in production.
    profiles_sample_rate=1.0,
)


#SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')
#SECURE_SSL_REDIRECT = True
#SESSION_COOKIE_SECURE = True
#CSRF_COOKIE_SECURE = True
