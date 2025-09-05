from .base import *

os.environ["ENVIRONMENT"] = "prod"

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = False

SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')
SECURE_SSL_REDIRECT = True

ALLOWED_HOSTS = [ FRONTEND_DOMAIN ]

CORS_ALLOWED_ORIGINS = [
    f"https://{FRONTEND_DOMAIN}"
]

# Database
# https://docs.djangoproject.com/en/5.2/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': os.environ['PROD_DB_NAME'],
        'USER': os.environ['PROD_DB_USER'],
        'PASSWORD': os.environ['PROD_DB_PASS'],
        'HOST': 'localhost',
        'PORT': 3306,
        'OPTIONS': {
                'charset': 'utf8mb4',
        },
        'CONN_MAX_AGE': 0
    }
}


