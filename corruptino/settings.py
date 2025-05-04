# corruptino/settings.py

import os
from pathlib import Path

# Loyiha katalogini belgilash
BASE_DIR = Path(__file__).resolve().parent.parent

# Xavfsizlik kaliti (haqiqiy loyiha uchun o'zgartirilishi kerak)
SECRET_KEY = 'django-insecure-abcdefghijklmnopqrstuvwxyz1234567890'

# Debug rejimi (ishlab chiqish uchun True, produkciya uchun False)
DEBUG = True

ALLOWED_HOSTS = []

# O'rnatilgan applar ro'yxati
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    # Tashqi applar
    'crispy_forms',
    'bootstrap4',
    'crispy_bootstrap4',

    # Loyiha applari
    'accounts',
    'jobs',
    'core',
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

ROOT_URLCONF = 'corruptino.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [
            os.path.join(BASE_DIR, 'core/templates'),
            os.path.join(BASE_DIR, 'accounts/templates'),  # Buni qo'shamiz
            os.path.join(BASE_DIR, 'jobs/templates'),      # Buni qo'shamiz
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

WSGI_APPLICATION = 'corruptino.wsgi.application'

# Ma'lumotlar bazasi sozlamalari
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}

# Parol tekshirish sozlamalari
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

# Til, vaqt mintaqasi va formatlash sozlamalari
LANGUAGE_CODE = 'uz-uz'
TIME_ZONE = 'Asia/Tashkent'
USE_I18N = True
USE_TZ = True

# Statik fayllar (CSS, JavaScript, rasmlar)
STATIC_URL = 'static/'
STATICFILES_DIRS = [os.path.join(BASE_DIR, 'static')]
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')

# Media fayllar (foydalanuvchi yuklagan fayllar)
MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

# Default primary key field
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# Custom user model (o'zimiz yaratgan model)
AUTH_USER_MODEL = 'accounts.User'

# Login va logout URL yo'llari
LOGIN_URL = 'accounts:login'
LOGIN_REDIRECT_URL = 'core:home'
LOGOUT_REDIRECT_URL = 'core:home'

# Crispy forms uchun shablon
CRISPY_TEMPLATE_PACK = 'bootstrap4'
CRISPY_ALLOWED_TEMPLATE_PACKS = ('bootstrap4',)