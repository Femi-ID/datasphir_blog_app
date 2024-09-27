"""
Django settings for blog_app project.

Generated by 'django-admin startproject' using Django 5.0.6.

For more information on this file, see
https://docs.djangoproject.com/en/5.0/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/5.0/ref/settings/
"""

from pathlib import Path
from datetime import timedelta
import dj_database_url
from decouple import config
import os

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/5.0/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
# SECRET_KEY = 'django-insecure-f36x^ypvpu9u^1^1p26cro@c0du)v7gn+g0wao2*a1i8d@ke79'
SECRET_KEY = os.environ.get('SECRET_KEY')
# SECRET_KEY = config("SECRET_KEY")

# SECURITY WARNING: don't run with debug turned on in production!
# DEBUG = True
DEBUG = os.environ.get('DEBUG')

# ALLOWED_HOSTS = []
ALLOWED_HOSTS = os.environ.get('ALLOWED_HOSTS').split(" ")

INTERNAL_IPS = [
    '127.0.0.1',
]

# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    # custom apps
    'users',
    'core',

     # added dependencies
    'rest_framework',
    # 'rest_framework_simplejwt',
    'djoser',
    'corsheaders',
    'rest_framework_swagger',   # Swagger
    'drf_yasg',
]

AUTH_USER_MODEL = 'users.User'

MIDDLEWARE = [
    "corsheaders.middleware.CorsMiddleware",
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',

    'whitenoise.middleware.WhiteNoiseMiddleware',
]

ROOT_URLCONF = 'blog_app.urls'

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

WSGI_APPLICATION = 'blog_app.wsgi.application'


# Database
# https://docs.djangoproject.com/en/5.0/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}
DATABASES['default'] = dj_database_url.parse('postgresql://blog_db_owner:DJXxorM1WPp3@ep-lively-king-a5rgpoas.us-east-2.aws.neon.tech/blog_db?sslmode=require')
# postgresql://blog_db_owner:DJXxorM1WPp3@ep-lively-king-a5rgpoas.us-east-2.aws.neon.tech/blog_db?sslmode=require

# Password validation
# https://docs.djangoproject.com/en/5.0/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/5.0/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/5.0/howto/static-files/

STATIC_URL = 'static/'

# Default primary key field type
# https://docs.djangoproject.com/en/5.0/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'


#  **************************************************************************************************

CORS_ALLOW_ALL_ORIGINS = True  # CHANGE THIS DURING PRODUCTION


REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework_simplejwt.authentication.JWTAuthentication',
    ),

    'DEFAULT_PERMISSION_CLASSES': (
        'rest_framework.permissions.IsAuthenticated',
    ),
}

# simple jwt configuration for  authorization header
SIMPLE_JWT = {
    'AUTH_HEADER_TYPES': ('JWT', 'Bearer'),
    'ACCESS_TOKEN_LIFETIME': timedelta(days=2)
}

DJOSER = {
    # sign up user
    'SEND_ACTIVATION_EMAIL': True,
    'SEND_CONFIRMATION_EMAIL': True,
    'PASSWORD_CHANGED_EMAIL_CONFIRMATION': True,
    'USER_CREATE_PASSWORD_RETYPE': True, # pass re-password to /users endpoint.
    'ACTIVATION_URL': 'auth/activate/{uid}/{token}', # url sent to the email to activate new user

    # reset user password
    'PASSWORD_RESET_CONFIRM_URL': 'password-reset/{uid}/{token}', # wil be appended to DOMAIN and sent to user email
    # 'SET_PASSWORD_RETYPE': True, # pass re_new_password to /users/set_password/ (when user creates new password)
    'PASSWORD_RESET_CONFIRM_RETYPE': True, # pass re_new_password to /users/reset_password_confirm/

    'SERIALIZERS': {
        # create  new user
        'user_create': 'users.serializers.UserCreateSerializer',

        # serializer view for general users and specific users
        'user': 'users.serializers.UserSerializer', # /users endpoint
        'current_user': 'users.serializers.UserSerializer', # /users/me endpoint
    },

}

SITE_NAME = 'DATASPHIR BLOG APP'
DOMAIN = 'rent-man.vercel.app' # (change to frontend localhost) the ACTIVATION_URL will be appended to this domain

# Email config
EMAIL_BACKEND = os.environ.get('EMAIL_BACKEND')
EMAIL_HOST = os.environ.get('EMAIL_HOST')
EMAIL_HOST_PASSWORD = os.environ.get('EMAIL_HOST_PASSWORD')
EMAIL_HOST_USER = os.environ.get('EMAIL_HOST_USER')
EMAIL_PORT = os.environ.get('EMAIL_PORT')
EMAIL_USE_TLS = os.environ.get('EMAIL_USE_TLS')
DEFAULT_FROM_EMAIL = os.environ.get('EMAIL_HOST_USER')

# EMAIL_BACKEND = config('EMAIL_BACKEND')
# EMAIL_HOST = config('EMAIL_HOST')
# EMAIL_HOST_PASSWORD = config('EMAIL_HOST_PASSWORD')
# EMAIL_HOST_USER = config('EMAIL_HOST_USER')
# EMAIL_PORT = config('EMAIL_PORT')
# EMAIL_USE_TLS = config('EMAIL_USE_TLS')
# # EMAIL_USE_SSL = config('EMAIL_USE_SSL')
# DEFAULT_FROM_EMAIL = config('EMAIL_HOST_USER')


SWAGGER_SETTINGS = {
   'SECURITY_DEFINITIONS': {
       'LOGIN_URL': 'http://127.0.0.1:8000/auth/jwt/create/',     # URL for login, e.g. /login/
    #    'LOGOUT_URL': 'your-logout-url',   # URL for logout, e.g. /logout/
       'USE_SESSION_AUTH': True,          # Use session authentication (Django Login)
      'Basic': {
            'type': 'oauth2'
      },
      'Bearer': {
            'type': 'apiKey',
            'name': 'Authorization',
            'in': 'header'
      },
      'DJANGO_LOGIN': ''
   }
}


CACHES = {
    "default": {
        "BACKEND": "django.core.cache.backends.redis.RedisCache",
        "LOCATION": "redis://127.0.0.1:6379",
        "TIMEOUT": 604800,
        # "OPTIONS": {"MAX_ENTRIES": 500}
    }
    # "default": {
    #     "BACKEND": "django.core.cache.backends.memcached.PyMemcacheCache", # Memcached binding
    #     "LOCATION": "127.0.0.1:11211", # Memcached is running on localhost (127.0.0.1) port 11211
    # }
}

REDIS_CLIENT_HOST = os.environ.get('REDIS_CLIENT_HOST')
REDIS_PORT = os.environ.get('REDIS_PORT')
REDIS_PASSWORD = os.environ.get('REDIS_PASSWORD')

# REDIS_CLIENT_HOST = config('REDIS_CLIENT_HOST')
# REDIS_PORT = config('REDIS_PORT')
# REDIS_PASSWORD = config('REDIS_PASSWORD')