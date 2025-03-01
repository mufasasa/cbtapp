"""
Django settings for project project.

Generated by 'django-admin startproject' using Django 5.0.2.

For more information on this file, see
https://docs.djangoproject.com/en/5.0/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/5.0/ref/settings/
"""

from pathlib import Path
from decouple import config
import os
import dj_database_url


# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/5.0/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'django-insecure-&6fj!azsjxrzw4p%lj)93ai!g(=p^sw!&803&i^ob2h-!p+c7_'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ['*']


# Application definition

INSTALLED_APPS = [
    'authentication',
    'rest_framework',
    'organisations_app',
    'candidates_app',
    'admin_app',
    'utills_app',
    'drf_yasg',
    'storages',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    "corsheaders",
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    "corsheaders.middleware.CorsMiddleware",
    "django.middleware.common.CommonMiddleware",
]

ROOT_URLCONF = 'project.urls'

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

WSGI_APPLICATION = 'project.wsgi.application'


# Database
# https://docs.djangoproject.com/en/5.0/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}

# DATABASES = {
#     'default': {
#         'ENGINE': 'django.db.backends.postgresql',
#         'NAME': config('DB_NAME'),
#         'USER': config('DB_USER'),
#         'PASSWORD': config('DB_PASSWORD'),
#         'HOST': config("DB_HOST"),
#         'PORT': config("DB_PORT"),
#     }
# }

# use database url if available in enviroment. else use one above

# DATABASES = {
#     'default': dj_database_url.parse(config('DATABASE_URL'))
# }


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

STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')


CORS_ORIGIN_ALLOW_ALL = True

CORS_ALLOW_ALL_ORIGINS=True

APPEND_SLASH = False


REST_FRAMEWORK = {
    'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.PageNumberPagination',
    'PAGE_SIZE': 10,  # You can set this to any number you prefer
}


# DigitalOcean Spaces Configuration
# USE_SPACES = True

# Spaces credentials
# SPACES_ACCESS_KEY_ID = config('SPACES_ACCESS_KEY_ID')
# SPACES_SECRET_ACCESS_KEY = config('SPACES_SECRET_ACCESS_KEY')

# # Spaces configurations
# SPACES_BUCKET_NAME = 'cbt-app-bucket-0'
# SPACES_REGION_NAME = 'fra1'  # Frankfurt region
# SPACES_ENDPOINT_URL = f'https://{SPACES_REGION_NAME}.digitaloceanspaces.com'
# SPACES_CDN_ENDPOINT_URL = f'https://{SPACES_BUCKET_NAME}.{SPACES_REGION_NAME}.cdn.digitaloceanspaces.com'

# # Django Storages Configuration
# AWS_ACCESS_KEY_ID = SPACES_ACCESS_KEY_ID  # django-storages uses AWS naming
# AWS_SECRET_ACCESS_KEY = SPACES_SECRET_ACCESS_KEY
# AWS_STORAGE_BUCKET_NAME = SPACES_BUCKET_NAME
# AWS_S3_ENDPOINT_URL = SPACES_ENDPOINT_URL
# AWS_S3_CUSTOM_DOMAIN = f'{SPACES_BUCKET_NAME}.{SPACES_REGION_NAME}.cdn.digitaloceanspaces.com'
# AWS_S3_OBJECT_PARAMETERS = {
#     'CacheControl': 'max-age=86400',
# }
# AWS_DEFAULT_ACL = 'public-read'
# AWS_LOCATION = 'media'

# # File Storage Configuration
# DEFAULT_FILE_STORAGE = 'storages.backends.s3boto3.S3Boto3Storage'
# MEDIA_URL = f'https://{AWS_S3_CUSTOM_DOMAIN}/{AWS_LOCATION}/'

# AWS_S3_OBJECT_PARAMETERS = {
#     'ACL': 'public-read',
#     'CacheControl': 'max-age=86400',
# }

# AWS_LOCATION = 'media'
# AWS_QUERYSTRING_AUTH = False 
