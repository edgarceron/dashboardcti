"""
Django settings for dashboardcti project.

Generated by 'django-admin startproject' using Django 3.0.4.

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
SECRET_KEY = '$vbq$=kx3c42ly_ji=$le=96f53$+0m6chg3yembzdil^-m!8b'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = []


# Application definition
WEB_APPS = [
    'users',
    'profiles',
    'dashboard',
    'agent_console',
    'form_creator',
    'motivos',
    'sedes',
    'asesores',
    'consolidacion'
]

WEB_APPS_LABELS = {
    'users' : 'Usuarios',
    'profiles' : 'Perfiles',
    'dashboard' : 'Dashboard',
    'agent_console' : 'Consola de agente',
    'form_creator' : 'Creador de formularios',
    'motivos': 'Motivos de entrada a taller',
    'sedes': 'Sedes',
    'asesores': 'Asesores de taller',
    'consolidacion': 'Consolidación de citas futuras',
}

INSTALLED_APPS = [
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'rest_framework',
    'maingui',
    'core',
    'dms'
]

INSTALLED_APPS += WEB_APPS

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'dashboardcti.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [
            '/maingui/templates/'
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

CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.memcached.MemcachedCache',
        'LOCATION': '127.0.0.1:11211',
    }
}

SESSION_ENGINE = 'django.contrib.sessions.backends.cache'

WSGI_APPLICATION = 'dashboardcti.wsgi.application'

# Database
# https://docs.djangoproject.com/en/3.0/ref/settings/#databases

# VOZIP
#call_center = {
#    'NAME': 'call_center',
#    'ENGINE': 'django.db.backends.mysql',
#    'USER': 'edgarceron',
#    'PASSWORD': 'firadankana',
#    'HOST': '200.29.111.108',
#    'PORT':'3306'
#}

# SG
#call_center = {
#    'NAME': 'call_center',
#    'ENGINE': 'django.db.backends.mysql',
#    'USER': 'testmanticore',
#    'PASSWORD': 'testmanticore',
#    'HOST': '10.163.100.5',
#    'PORT':'3306'
#}

# CARIBE
call_center = {
    'NAME': 'call_center',
    'ENGINE': 'django.db.backends.mysql',
    'USER': 'desarrollo',
    'PASSWORD': 'firadankana',
    'HOST': '192.168.1.252',
    'PORT':'3306'
}

caribe_dms = {
    'ENGINE': 'sql_server.pyodbc',
    'NAME': 'CARIBE1',
    'HOST': "192.168.1.246",
    'PORT': '1433',
    'USER': 'vozip',
    'PASSWORD': 'V0z1p2020',
    'OPTIONS': {
        'driver': 'ODBC Driver 17 for SQL Server',
    }
}

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'dashboardcti',
        'USER': 'vozip',
        'PASSWORD': 'rVozip301',
        'HOST': 'localhost',
        'PORT': '5432',
    },

    'call_center': call_center,
    #'caribe_dms': caribe_dms
}

DATABASE_ROUTERS = ['dashboard.dbrouters.router.IntegrationRouter']
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

PASSWORD_HASHERS = [
    'django.contrib.auth.hashers.PBKDF2PasswordHasher',
]

REST_FRAMEWORK = {}

SILENCED_SYSTEM_CHECKS = ["models.W027"]
# Internationalization
# https://docs.djangoproject.com/en/3.0/topics/i18n/

LANGUAGE_CODE = 'es-es'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/3.0/howto/static-files/

STATIC_URL = '/static/'

# Email settings
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_PORT = '587'
EMAIL_HOST_USER = 'edgar.mauricio.ceron@gmail.com'
EMAIL_HOST_PASSWORD = 'firadankana'
EMAIL_USE_TLS = True
EMAIL_USE_SSL = False

# Channels setting for Websocket support

#ASGI_APPLICATION = 'dashboardcti.asgi.application'

#CHANNEL_LAYERS = {
#    'default': {
#        'BACKEND': 'channels_redis.core.RedisChannelLayer',
#        'CONFIG': {
#            "hosts": [('127.0.0.1', 6379)],
#       },
#    },
#}