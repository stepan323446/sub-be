from .base import *

os.environ["ENVIRONMENT"] = "dev"

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

CORS_ALLOWED_ORIGINS = [
    "http://localhost:8080",
    "http://127.0.0.1:8000",
]

# Database
# https://docs.djangoproject.com/en/5.2/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}

ACTIVATION_PATTERN_URL_FRONTEND = 'https://localhost:8001/activate/<code>'
RESET_PASS_PATTERN_URL_FRONTEND = 'https://localhost:8001/reset/<code>'
