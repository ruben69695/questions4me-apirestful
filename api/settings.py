"""
Django settings for api project.

Generated by 'django-admin startproject' using Django 3.0.2.

For more information on this file, see
https://docs.djangoproject.com/en/3.0/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/3.0/ref/settings/
"""

import os

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/3.0/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = '(golt31^o-+g0my0^7-4n3k@i8!-dby(os*n!d(3_ro944yen4'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

# DEPLOYMENT: don't run with azure turned on if you are not ready to deploy it on azure
AZURE = False

ALLOWED_HOSTS = ['*']


# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'rest_framework',
    'corsheaders',
    'api.app',
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

ROOT_URLCONF = 'api.urls'

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

WSGI_APPLICATION = 'api.wsgi.application'


# Database
# https://docs.djangoproject.com/en/3.0/ref/settings/#databases

if AZURE:
    # Using Azure Key Vault to Retrieve Secrets for database connection
    from azure.keyvault.secrets import SecretClient
    from azure.core.exceptions import HttpResponseError
    from msrestazure.azure_active_directory import MSIAuthentication
    import sys

    # Create MSI Authentication
    credentials = MSIAuthentication()

    key_vault_url = os.environ['Questions4MeVaultUrl']

    client = SecretClient(key_vault_url, credentials)
    
    if key_vault_url is None:
        raise Exception('Key Vault Url not found as environment variable')
    
    # Get Host Secret
    secret_host_keyname = 'PostgresHost'
    host_secret_bundle = client.get_secret(secret_host_keyname, version='a2a018e3dea3457e9e21674054dbe2ff')

    # Get User Secret
    secret_user_keyname = 'PostgresUserName'
    user_secret_bundle = client.get_secret(secret_user_keyname, version='eae4650dffa3466b97bbc733009f7647')

    # Get Password Secret
    secret_password_keyname = 'PostgresPassword'
    password_secret_bundle = client.get_secret(secret_password_keyname, version='a9e48977f66641efb456120d7036fd15')

    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.postgresql_psycopg2',
            'NAME': 'postgres',
            'USER': user_secret_bundle.value,
            'PASSWORD': password_secret_bundle.value,
            'HOST': host_secret_bundle.value,
            'PORT': '5432'
        }
    }
else:
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
        }
    }


# Password validation
# https://docs.djangoproject.com/en/3.0/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/3.0/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.9/howto/static-files/
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')
STATIC_URL = '/staticfiles/'


CORS_ORIGIN_WHITELIST = [
    "http://localhost:3000",
    "http://127.0.0.1:3000"
]


# Configure Django App for Heroku.
import django_heroku
django_heroku.settings(locals())