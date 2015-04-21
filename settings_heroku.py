from settings_common import *

# ===========================
# = Directory Declaractions =
# ===========================
import dj_database_url

PROJECT_PATH = os.path.dirname(os.path.abspath(__file__))

# this url will be prepended to all the menus urls where
# QR codes for are generated
HOST_URL = "HTTP://ZINQ.HEROKUAPP.COM/"
MENU_URL = HOST_URL + "MENU/"


DEBUG = False
TEMPLATE_DEBUG = DEBUG

ADMINS = (
    ('Ward Coessens', 'ward.coessens@gmail.com'),
)

MANAGERS = ADMINS


# Python dotted path to the WSGI application used by Django's runserver.
WSGI_APPLICATION = 'wsgi.application'


INSTALLED_APPS = (
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.sites',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'bootstrap_toolkit',
    'places',
    'menus',
    # Bootstrap django admin
    # 'django_admin_bootstrapped',
    #  Uncomment the next line to enable the admin, with grappelli skin
    'grappelli',
    'django.contrib.admin',
    # Uncomment the next line to enable admin documentation:
    'django.contrib.admindocs',
    # 'debug_toolbar',
    'qrcode',
)

# A sample logging configuration. The only tangible logging
# performed by this configuration is to send an email to
# the site admins on every HTTP 500 error when DEBUG=False.
# See http://docs.djangoproject.com/en/dev/topics/logging for
# more details on how to customize your logging configuration.

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'simple': {
            'format': '%(levelname)s %(message)s'
        },
    },
    'filters': {
        'require_debug_false': {
            '()': 'django.utils.log.RequireDebugFalse'
        }
    },
    'handlers': {
        'console': {
            'level': 'DEBUG',
            'class': 'logging.StreamHandler',
            'formatter': 'simple'
        },
    },
    'loggers': {
        'places': {
            'handlers': ['console'],
            'level': 'DEBUG',
        },
        'menus': {
            'handlers': ['console'],
            'level': 'DEBUG',
        },
        'orders': {
            'handlers': ['console'],
            'level': 'DEBUG',
        }
    }
}


DATABASES = {}

DATABASES['default'] = dj_database_url.config()

# Honor the 'X-Forwarded-Proto' header for request.is_secure()
SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')

# Allow all host headers
ALLOWED_HOSTS = ['*']


# strungling with STATIC files on Heroku. Setting it to their settings
# Configuring static as per https://devcenter.heroku.com/articles/django-assets
STATIC_ROOT = 'staticfiles'
STATIC_URL = '/static/'

STATICFILES_DIRS = (
    os.path.join(PROJECT_PATH, 'media'),
)
