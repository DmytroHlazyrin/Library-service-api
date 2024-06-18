import sys
from datetime import timedelta
from pathlib import Path

import dj_database_url
from celery.schedules import crontab
from decouple import config

BASE_DIR = Path(__file__).resolve().parent.parent
SECRET_KEY = config("DJANGO_SECRET_KEY")

DEBUG = True

ALLOWED_HOSTS = [
    "localhost",
    "127.0.0.1",
]

INTERNAL_IPS = [
    "127.0.0.1",
]

# Application definition

INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "rest_framework",
    "rest_framework_simplejwt",
    "drf_spectacular",
    "django_celery_beat",

    # apps
    "user",
    "book",
    "borrowing",
    "payment",
]

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

REST_FRAMEWORK = {
    "DEFAULT_AUTHENTICATION_CLASSES": (
        "rest_framework_simplejwt.authentication.JWTAuthentication",
    ),
    "DEFAULT_SCHEMA_CLASS": "drf_spectacular.openapi.AutoSchema",
    "DEFAULT_PAGINATION_CLASS": (
        "rest_framework.pagination.PageNumberPagination"
    ),
    "PAGE_SIZE": 5,
}

SIMPLE_JWT = {
    "ACCESS_TOKEN_LIFETIME": timedelta(minutes=1000),
    "REFRESH_TOKEN_LIFETIME": timedelta(days=1),
    "ROTATE_REFRESH_TOKENS": False,
}

SPECTACULAR_SETTINGS = {
    "TITLE": "Book Rental Service",
    "DESCRIPTION": "Borrow books to read!",
    "VERSION": "1.0.0",
    "SERVE_INCLUDE_SCHEMA": False,
    "SWAGGER_UI_SETTINGS": {
        "deepLinking": True,
        "defaultModelRendering": "model",
        "defaultModelsExpandDepth": 2,
        "defaultModelExpandDepth": 2,
    },
}

TESTING = "test" in sys.argv

if not TESTING:
    INSTALLED_APPS += [
        "debug_toolbar",
    ]
    MIDDLEWARE += [
        "debug_toolbar.middleware.DebugToolbarMiddleware",
    ]
    REST_FRAMEWORK.update({
        "DEFAULT_THROTTLE_CLASSES": [
            "rest_framework.throttling.AnonRateThrottle",
            "rest_framework.throttling.UserRateThrottle",
        ],
        "DEFAULT_THROTTLE_RATES": {
            "anon": "10/minute",
            "user": "30/minute",
        },
    })

ROOT_URLCONF = "library_service.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    },
]

WSGI_APPLICATION = "library_service.wsgi.application"

DATABASE_URL = config("DATABASE_URL", default="sqlite:///db.sqlite3")

DATABASES = {"default": dj_database_url.parse(DATABASE_URL, conn_max_age=600)}

AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": "django.contrib.auth."
                "password_validation.UserAttributeSimilarityValidator",
    },
    {
        "NAME": "django.contrib.auth."
                "password_validation.MinimumLengthValidator",
    },
    {
        "NAME": "django.contrib.auth."
                "password_validation.CommonPasswordValidator",
    },
    {
        "NAME": "django.contrib.auth."
                "password_validation.NumericPasswordValidator",
    },
]

LANGUAGE_CODE = "en-us"

TIME_ZONE = "UTC"

USE_I18N = True

USE_TZ = True

STATIC_URL = "static/"

MEDIA_ROOT = BASE_DIR / "media/"

MEDIA_URL = "/media/"

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

AUTH_USER_MODEL = "user.User"

STRIPE_PUBLISHABLE_KEY = config("STRIPE_PUBLISHABLE_KEY")
STRIPE_SECRET_KEY = config("STRIPE_SECRET_KEY")

CELERY_BROKER_URL = "redis://redis:6379/0"
CELERY_RESULT_BACKEND = "redis://redis:6379/0"

CELERY_BEAT_SCHEDULE = {
    "expired_payment_sessions_task": {
        "task": "payment.tasks.check_stripe_sessions",
        "schedule": crontab(minute="*/1")
    },
    "borrowing_expired_task": {
        "task": "borrowing.tasks.get_borrowing_report",
        "schedule": crontab(hour=15, minute=0)
    },
    "daily_payment_report_task": {
        "task": "payment.tasks.daily_payment_report",
        "schedule": crontab(hour=19, minute=0)
    },
    "monthly_payment_report_task": {
        "task": "payment.tasks.monthly_payment_report",
        "schedule": crontab(hour=9, minute=0, day_of_month=1)
    }
}
