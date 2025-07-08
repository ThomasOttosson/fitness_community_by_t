import os
from pathlib import Path

import dj_database_url
import stripe

if os.path.isfile('env.py'):
    import env

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# --------------------------------------------------------------------------- #
# Core settings
# --------------------------------------------------------------------------- #
SECRET_KEY = os.environ.get('SECRET_KEY')

DEBUG = True

# settings.py – temporary!
# DEBUG_PROPAGATE_EXCEPTIONS = True

ALLOWED_HOSTS = [
    '.herokuapp.com',
    '127.0.0.1',
    'localhost',
]

CSRF_TRUSTED_ORIGINS = [
    'https://*.codeinstitute-ide.net',
    'https://*.herokuapp.com',
]


# --------------------------------------------------------------------------- #
# Application definition
# --------------------------------------------------------------------------- #
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.sitemaps',
    'fitness',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'fitness_community_by_t.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'templates'],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

MESSAGE_STORAGE = 'django.contrib.messages.storage.fallback.FallbackStorage'

WSGI_APPLICATION = 'fitness_community_by_t.wsgi.application'


# --------------------------------------------------------------------------- #
# Database
# --------------------------------------------------------------------------- #
DATABASES = {
    'default': dj_database_url.parse(str(os.environ.get("DATABASE_URL")))
}


# --------------------------------------------------------------------------- #
# Password validation
# --------------------------------------------------------------------------- #
AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': (
            'django.contrib.auth.password_validation.'
            'UserAttributeSimilarityValidator'
        ),
    },
    {
        'NAME': (
            'django.contrib.auth.password_validation.MinimumLengthValidator'
        ),
    },
    {
        'NAME': (
            'django.contrib.auth.password_validation.CommonPasswordValidator'
        ),
    },
    {
        'NAME': (
            'django.contrib.auth.password_validation.NumericPasswordValidator'
        ),
    },
]


# --------------------------------------------------------------------------- #
# Internationalisation
# --------------------------------------------------------------------------- #
LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'UTC'
USE_I18N = True
USE_TZ = True


# --------------------------------------------------------------------------- #
# Static & media files
# --------------------------------------------------------------------------- #
STATIC_URL = 'static/'
STATIC_ROOT = BASE_DIR / 'staticfiles'
STATICFILES_DIRS = [BASE_DIR / 'static']

MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / 'media'

STORAGES = {
    'default': {
        'BACKEND': 'django.core.files.storage.FileSystemStorage',
    },
    'staticfiles': {
        'BACKEND': (
            'whitenoise.storage.CompressedManifestStaticFilesStorage'
        ),
    },
}

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'


# --------------------------------------------------------------------------- #
# Authentication redirects
# --------------------------------------------------------------------------- #
LOGIN_REDIRECT_URL = '/accounts/profile/'
LOGOUT_REDIRECT_URL = '/'


# --------------------------------------------------------------------------- #
# Stripe
# --------------------------------------------------------------------------- #
STRIPE_PUBLISHABLE_KEY = os.getenv('STRIPE_PUBLISHABLE_KEY')
STRIPE_SECRET_KEY = os.getenv('STRIPE_SECRET_KEY')

if STRIPE_SECRET_KEY:
    stripe.api_key = STRIPE_SECRET_KEY


# --------------------------------------------------------------------------- #
# Mailchimp
# --------------------------------------------------------------------------- #
MAILCHIMP_API_KEY = os.getenv('MAILCHIMP_API_KEY')
MAILCHIMP_AUDIENCE_ID = os.getenv('MAILCHIMP_AUDIENCE_ID')
MAILCHIMP_SERVER_PREFIX = os.getenv('MAILCHIMP_SERVER_PREFIX')
