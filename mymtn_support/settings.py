"""
Django settings for mymtn_support project.

AI-Enhanced Customer Support System for myMTN NG Mobile Application
Generated based on TGO design patterns and Chapter 3 requirements.
"""

from pathlib import Path
from datetime import timedelta

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'django-insecure-mymtn-support-system-2025-change-in-production'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ['*']


# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    
    # Third-party apps
    'rest_framework',
    'corsheaders',
    'channels',
    
    # Local apps
    'core',
    'chat',
    'visitors',
    'nlp_service',
    'knowledge_base',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'mymtn_support.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'frontend' / 'build'],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'mymtn_support.wsgi.application'

# Channels configuration for WebSocket support
ASGI_APPLICATION = 'mymtn_support.asgi.application'

# Channel layers configuration (using in-memory for development, Redis for production)
CHANNEL_LAYERS = {
    'default': {
        'BACKEND': 'channels.layers.InMemoryChannelLayer'
    }
}


# Database
# https://docs.djangoproject.com/en/6.0/ref/settings/#databases

# Using SQLite for local development (built-in Django database)
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}

# For production with PostgreSQL (uncomment to use PostgreSQL)
# DATABASES = {
#     'default': {
#         'ENGINE': 'django.db.backends.postgresql',
#         'NAME': 'mymtn_support_db',
#         'USER': 'mymtn_user',
#         'PASSWORD': 'mymtn_password',
#         'HOST': 'localhost',
#         'PORT': '5432',
#     }
# }


# Password validation
# https://docs.djangoproject.com/en/6.0/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]


# Internationalization
# https://docs.djangoproject.com/en/6.0/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'Africa/Lagos'

USE_I18N = True

USE_TZ = True

# Supported languages for multilingual support
LANGUAGES = [
    ('en', 'English'),
    ('yo', 'Yoruba'),
    ('ha', 'Hausa'),
    ('ig', 'Igbo'),
    ('pcm', 'Nigerian Pidgin'),
]

LOCALE_PATHS = [
    BASE_DIR / 'locale',
]


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/6.0/howto/static-files/

STATIC_URL = 'static/'
STATIC_ROOT = BASE_DIR / 'staticfiles'
STATICFILES_DIRS = [
    BASE_DIR / 'frontend' / 'build' / 'static',
]

# Media files
MEDIA_URL = 'media/'
MEDIA_ROOT = BASE_DIR / 'media'


# Default primary key field type
# https://docs.djangoproject.com/en/6.0/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'


# REST Framework configuration
REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': [
        'rest_framework.authentication.SessionAuthentication',
        'rest_framework.authentication.BasicAuthentication',
    ],
    'DEFAULT_PERMISSION_CLASSES': [
        'rest_framework.permissions.IsAuthenticatedOrReadOnly',
    ],
    'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.PageNumberPagination',
    'PAGE_SIZE': 20,
}


# CORS configuration
CORS_ALLOWED_ORIGINS = [
    'http://localhost:3000',
    'http://localhost:5173',
    'http://127.0.0.1:3000',
    'http://127.0.0.1:5173',
]

CORS_ALLOW_CREDENTIALS = True


# Custom user model
AUTH_USER_MODEL = 'core.Staff'


# Session configuration
SESSION_ENGINE = 'django.contrib.sessions.backends.db'
SESSION_COOKIE_AGE = 3600  # 1 hour
SESSION_SAVE_EVERY_REQUEST = True


# NLP Service Configuration
NLP_SERVICE = {
    'MODEL_NAME': 'AfroXLMR',
    'INTENT_THRESHOLD': 0.75,
    'ENTITY_THRESHOLD': 0.70,
    'SUPPORTED_INTENTS': [
        'check_balance',
        'buy_data',
        'buy_airtime',
        'subscribe_plan',
        'complaint',
        'greeting',
        'escalate_to_human',
    ],
    'SUPPORTED_LANGUAGES': ['en', 'yo', 'ha', 'ig', 'pcm'],
}


# Chat configuration
CHAT_CONFIG = {
    'MAX_MESSAGE_LENGTH': 2000,
    'TYPING_TIMEOUT': 5,  # seconds
    'SESSION_TIMEOUT': 1800,  # 30 minutes
    'AUTO_ASSIGN_ENABLED': True,
    'MAX_QUEUE_WAIT_TIME': 300,  # 5 minutes
}


# Escalation configuration
ESCALATION_CONFIG = {
    'MAX_AI_RETRIES': 3,
    'CONFIDENCE_THRESHOLD': 0.6,
    'AUTO_ESCALATE_INTENTS': ['complaint', 'urgent'],
}
