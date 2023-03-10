from pathlib import Path

import os

from dotenv import load_dotenv


load_dotenv()
KEY_MAIL = os.getenv('KEY_MAIL')

print(KEY_MAIL)

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/4.1/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'django-insecure-b+tzq-l4cgih!-zyo@24#qln4tp#b-8r*f=imrgjtu=+wcmqrz'

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

    'rest_framework',  # djangorestframework
    'rest_framework.authtoken', # Для использования стандартной библиотеки авторизации по токенам
    'djoser',
    "debug_toolbar",
    'captcha',
    # 'rest_framework_swagger',
    'drf_yasg',

    'blog',
    'mailcontact',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',

    'blog.middleware.CurrentRequestMiddlewareUser',

    "debug_toolbar.middleware.DebugToolbarMiddleware",
]

ROOT_URLCONF = 'config.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'templates']
        ,
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
# https://docs.djangoproject.com/en/4.1/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}


# Password validation
# https://docs.djangoproject.com/en/4.1/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    # {
    #     'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    # },
    # {
    #     'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    # },
    # {
    #     'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    # },
    # {
    #     'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    # },
]


# Internationalization
# https://docs.djangoproject.com/en/4.1/topics/i18n/

LANGUAGE_CODE = 'ru'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.1/howto/static-files/

MEDIA_ROOT = os.path.join(BASE_DIR, 'media') # Here
MEDIA_URL = '/media/'

STATIC_URL = 'static/'
# Указываем куда сохранять статику:
STATIC_ROOT = os.path.join(BASE_DIR, 'static')
# Указываем откуда собирать статику:
STATICFILES_DIRS = [
    os.path.join(BASE_DIR, 'blog/static'),
]

# Default primary key field type
# https://docs.djangoproject.com/en/4.1/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

REST_FRAMEWORK = {
    'DEFAULT_PERMISSION_CLASSES': ( # Кто имеет доступ
        'rest_framework.permissions.IsAdminUser', # Администратор
        'rest_framework.permissions.AllowAny', # Все
    ),
    # 'PAGE_SIZE': 10, # Пагинация
    'DEFAULT_AUTHENTICATION_CLASSES': [ # Аутентификация
        # 'rest_framework_jwt.authentication.JSONWebTokenAuthentication', # Для JWT регистрации
        'rest_framework.authentication.TokenAuthentication', # по токену Для Djoser
        'rest_framework.authentication.BasicAuthentication', # Базовая
        'rest_framework.authentication.SessionAuthentication' # Для session, например что бы зайти в админку
    ],
    # Настройка рендера для отправки на фронт и получение на бэк в JSON
    # 'DEFAULT_RENDERER_CLASSES': (
    #     'rest_framework_json_api.renderers.JSONRenderer',
    #     'rest_framework.renderers.BrowsableAPIRenderer',
    # ),
    # 'DEFAULT_METADATA_CLASS': 'rest_framework_json_api.metadata.JSONAPIMetadata',
}

INTERNAL_IPS = [
    "127.0.0.1",
]

LOGIN_URL = '/login/'

# EMAIL
EMAIL_HOST = 'smtp.mail.ru'
EMAIL_PORT = 465
EMAIL_HOST_USER = 'chausovo@mail.ru' # Почта отправителя
EMAIL_HOST_PASSWORD = KEY_MAIL # Пароль для внешнего приложения
EMAIL_USE_TLS = False # Шифрование TSL
EMAIL_USE_SSL = True # Шифрование SSL

# Для вывода ORM запросов в консоль
LOGGING = {
    'version': 1,
    'handlers': {
        'console': {'class': 'logging.StreamHandler'},
    },
    'loggers': {
        'django.db.backends': {
            'handlers': ['console'],
            'level': 'DEBUG'
            }
        }
}
