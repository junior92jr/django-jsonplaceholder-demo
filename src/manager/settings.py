from pathlib import Path
from datetime import timedelta
from os import getenv as os_getenv, path as os_path  # noqa

from django.core.management.utils import get_random_secret_key


BASE_DIR = Path(__file__).resolve().parent.parent

SECRET_KEY = os_getenv(
    "SECRET_KEY", get_random_secret_key()
)

DEBUG = os_getenv("DEBUG", "true").lower() in ["True", "true", "1", "yes", "y"]

ALLOWED_HOSTS = os_getenv("ALLOWED_HOSTS", "localhost").split(",")

# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'rest_framework',
    'rest_framework_simplejwt',
    'django_filters',
    'django_crontab',
    'posts',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'manager.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
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

WSGI_APPLICATION = 'manager.wsgi.application'


# Database
# https://docs.djangoproject.com/en/4.2/ref/settings/#databases

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql",
        "NAME": os_getenv("POSTGRES_DB", "postgres"),
        "USER": os_getenv("POSTGRES_USER", "postgres"),
        "PASSWORD": os_getenv("POSTGRES_PASSWORD", "postgres"),
        "HOST": os_getenv("POSTGRES_HOST", "db"),
        "PORT": os_getenv("POSTGRES_PORT", "5432"),
    }
}


# Password validation
# https://docs.djangoproject.com/en/4.2/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator', # noqa
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator', # noqa
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator', # noqa
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator', # noqa
    },
]


# Internationalization
# https://docs.djangoproject.com/en/4.2/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'CET'

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.2/howto/static-files/

STATIC_URL = 'static/'

# Default primary key field type
# https://docs.djangoproject.com/en/4.2/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

DEFAULT_EXTERNAL_USER_ID = 99999942

# Django Rest Framework

REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework_simplejwt.authentication.JWTAuthentication',), # noqa
    'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.PageNumberPagination', # noqa
    'PAGE_SIZE': 10,
}

SIMPLE_JWT = {
    'ACCESS_TOKEN_LIFETIME': timedelta(minutes=5),
    'REFRESH_TOKEN_LIFETIME': timedelta(days=1),
}

CRONJOBS = [
    (
        '0 0 * * *',
        'posts.tasks.sync_posts.syncronize_posts_task',
        '>> /cron/django_cron.log 2>&1'
    ),
    (
        '0 1 * * *',
        'posts.tasks.sync_comments.syncronize_comments_task',
        '>> /cron/django_cron.log 2>&1'
    ),
]

# Logging settings
LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    "formatters": {
        "simple": {
            "format": "[%(asctime)s] %(levelname)s|%(name)s|%(message)s",
            "datefmt": "%Y-%m-%d %H:%M:%S",
        },
    },
    "handlers": {
        "console": {
            "level": 'INFO',
            "class": "logging.StreamHandler",
            "formatter": "simple"
        },
    },
    "root": {
        "handlers": ["console"],
        "level": "INFO",
    },
    "loggers": {
        "django": {
            "handlers": ["console"],
            "level": "INFO",
            "propagate": False,
        },
    },
}
