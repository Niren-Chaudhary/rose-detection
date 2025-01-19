import os
from pathlib import Path
from datetime import timedelta
import mongoengine
# import environ

# # Initialize the environment variables
# env = environ.Env()
# environ.Env.read_env()  # Read the .env file

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

# Quick-start development settings - unsuitable for production
# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'django-insecure-k%fq=4k29a_6i@x0w2i-95oq%%q60h3@i2!8%u5zun@e&@snh^'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = []

# Application definition
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'rest_framework',  # Django REST Framework
    #'rest_framework.authtoken',  # Token authentication
    'api',  # Replace with your app name
    'corsheaders',  # CORS handling
    'rest_framework_simplejwt',  # For JWT authentication
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.common.CommonMiddleware',
]

ROOT_URLCONF = 'djangobackend.urls'

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

WSGI_APPLICATION = 'djangobackend.wsgi.application'

# MongoDB Configuration using MongoEngine
mongoengine.connect(
    db="rosedata",  # Your MongoDB database name
    host="mongodb+srv://ravipant1122:1122@cluster0.ef1rf.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0",  # MongoDB URI
)

# Password validation
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

# REST Framework settings
REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': [
        'rest_framework_simplejwt.authentication.JWTAuthentication',  # Use JWT authentication
    ],
    'DEFAULT_PERMISSION_CLASSES': [
        'rest_framework.permissions.IsAuthenticated',  # Restrict access to authenticated users
    ],
}

SIMPLE_JWT = {
    'ACCESS_TOKEN_LIFETIME': timedelta(minutes=30),
    'REFRESH_TOKEN_LIFETIME': timedelta(days=1),
    'ROTATE_REFRESH_TOKENS': False,
    'BLACKLIST_AFTER_ROTATION': False,
}

# Internationalization
LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'UTC'
USE_I18N = True
USE_TZ = True

# Static files (CSS, JavaScript, Images)
STATIC_URL = 'static/'

# Media files (User-uploaded content)
MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

# Default primary key field type
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# CORS handling
CORS_ALLOW_ALL_ORIGINS = True

# If you want to specify only the Flutter web app origin
CORS_ALLOWED_ORIGINS = [
    "http://127.0.0.1:8000",  # Django server
    "http://127.0.0.1:59394",  # Flutter app in DevTools
]

# Allow specific HTTP methods and headers if needed
CORS_ALLOW_METHODS = [
    "GET",
    "POST",
    "PUT",
    "DELETE",
    "PATCH",
    "OPTIONS",
]

CORS_ALLOW_HEADERS = [
    "content-type",
    "authorization",
    "x-csrftoken",
    "x-requested-with",
]

# # Email configuration using environment variables
# EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
# EMAIL_HOST = env('EMAIL_HOST')  # Will be fetched from .env
# EMAIL_PORT = env('EMAIL_PORT')  # Will be fetched from .env
# EMAIL_USE_TLS = env('EMAIL_USE_TLS')  # Will be fetched from .env
# EMAIL_HOST_USER = env('EMAIL_HOST_USER')  # Will be fetched from .env
# EMAIL_HOST_PASSWORD = env('EMAIL_HOST_PASSWORD')  # Will be fetched from .env

# Set Custom User Model (MongoEngine doesn't use the Django ORM model)
# AUTH_USER_MODEL = 'api.CustomUser'  # Replace 'yourapp' with the actual app name

CORS_ALLOW_ALL_ORIGINS = True
AUTHENTICATION_BACKENDS = [
    'api.auth_backends.MongoEngineBackend',
    'django.contrib.auth.backends.ModelBackend',
]
