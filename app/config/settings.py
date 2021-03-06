"""
Django settings for config project.

Generated by 'django-admin startproject' using Django 2.1.2.

For more information on this file, see
https://docs.djangoproject.com/en/2.1/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/2.1/ref/settings/
"""
import json
import os

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

ROOT_DIR = os.path.dirname(BASE_DIR)
SECRETS_DIR = os.path.join(ROOT_DIR, '.secrets')
secrets = json.load(open(os.path.join(SECRETS_DIR, 'base.json')))

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/2.1/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = '+$hbkov)a_kup&8)+5sydr2%u5*-n9@g%z#v^fb#qrx+xs@m!&'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = []


EMAIL_BACKEND = secrets['EMAIL_BACKEND']
EMAIL_HOST = secrets['EMAIL_HOST']
EMAIL_HOST_USER = secrets['EMAIL_HOST_USER']
EMAIL_HOST_PASSWORD = secrets['EMAIL_HOST_PASSWORD']
EMAIL_USE_TLS: True
EMAIL_USER_SSL: True

# Application definition

INSTALLED_APPS = [
    'blog',
    'accounts',

    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    'django_extensions',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'accounts.middleware.KickMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'accounts.middleware.KickedMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'config.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [
            os.path.join(BASE_DIR, 'config', 'templates'),
        ],
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

WSGI_APPLICATION = 'config.wsgi.application'


# Database
# https://docs.djangoproject.com/en/2.1/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
}


# Password validation
# https://docs.djangoproject.com/en/2.1/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/2.1/topics/i18n/

LANGUAGE_CODE = 'ko-kr'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/2.1/howto/static-files/

STATIC_URL = '/static/'


from django.urls import reverse_lazy

AUTH_USER_MODEL = 'accounts.User'

# url 주소에 reverse 함수를 사용하여 주소를 전달
# reverse_lazy = lazy(reverse, str)
LOGIN_URL = reverse_lazy('login')
# LOGIN_REDIRECT_URL = reverse_lazy('profile')

# 로그아웃 후에 next 페이지를 지정해주지 않을 경우 아래의 변수가 실행됨
#   이는 logoutview 에 동일한 변수가 있음
#   현재는 템플릿에서 직접 파라미터로 ?next={{ request.path }} 를 지정하여
#   보고 있는 현재 페이지로 다시 리다이렉트 되도록 설정(1순위)
#       만약 1순위를 설정하지 않을 경우에는 아래의 경로로 리다이렉트 됨
LOGOUT_REDIRECT_URL = reverse_lazy('login')
