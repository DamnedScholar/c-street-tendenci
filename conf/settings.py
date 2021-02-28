import json
import os
from django import __path__ as django_path

from tools.modulation.utils import Registry
lib = Registry('lib')
tools = Registry('tools')


# Load secret and server-specific settings so that we can sync `settings.py`
# TODO: Replace this with a .env file.
with open('conf/secrets.json') as f:
    secrets = json.load(f)

# ---------------------------------------------------------------------------- #
# Debug Setting
# ---------------------------------------------------------------------------- #

# To enable verbose error pages, debug logging, and other features that are
# useful for development/testing but should not be enabled on live sites,
# uncomment this setting.
DEBUG = True

# if DEBUG:
#     disable_template_cache()


# ---------------------------------------------------------------------------- #
# Misc Site-Specific Settings
# ---------------------------------------------------------------------------- #

# Any site-specific settings that do not fit in the sections below can go here.

ASGI_APPLICATION = 'sockpuppet.routing.application'

CHANNEL_LAYERS = {
    "default": {
        "BACKEND": "channels.layers.InMemoryChannelLayer"
    }
}


# ---------------------------------------------------------------------------- #
# Required Settings
# ---------------------------------------------------------------------------- #

# This is for the Sites framework.
SITE_ID = 1

# These must be set to two different random strings, at least 50 characters in
# length, that are unique to this site.  Django will refuse to start if these
# are not configured.
# The security of the site relies on these being appropriately random, so use a
# good random number generator.  Good random strings are conveniently available
# at https://www.grc.com/passwords.htm (Use the
# "63 random alpha-numeric characters" string, and refresh the page to get an
# additional string.)
SECRET_KEY = secrets['secret_key']
SITE_SETTINGS_KEY = secrets['site_settings_key']

# This must be set to a list of fully qualified domain names that are valid for
# this site.  Connections which request any other name will be rejected.
# To prevent HTTP Host header attacks, this list must be limited to names that
# are actually hosted on this server.
# If this server uses a wildcard DNS record then you can prefix the domain
# listed here with a '.' to match all subdomains ('.example.com').
ALLOWED_HOSTS = secrets['allowed_hosts']
if DEBUG:
    ALLOWED_HOSTS += secrets['allowed_hosts_debug']

# Tendenci uses the following PostgreSQL database connection settings by
# default.  Uncomment and configure settings here to override the defaults.
DATABASES = {
    'default': {
        'ENGINE': 'django.contrib.gis.db.backends.postgis',
        'HOST': secrets['databases']['default']['host'],
        'PORT': secrets['databases']['default']['port'],
        'USER': secrets['databases']['default']['user'],
        'PASSWORD': secrets['databases']['default']['password'],
        'NAME': secrets['databases']['default']['name'],
    }
}

# This must be set to the time zone used by PostgreSQL, which defaults to the
# system time zone configured in /etc/timezone.
# To change the PostgreSQL time zone without changing the system time zone:
# sudo -u postgres psql -c "ALTER ROLE $DB_USER SET timezone TO 'US/Eastern';"
# A list of time zone names can be found at
# http://en.wikipedia.org/wiki/List_of_tz_zones_by_name
TIME_ZONE = 'US/Central'


# ---------------------------------------------------------------------------- #
# Auth0 Settings
# ---------------------------------------------------------------------------- #

SOCIAL_AUTH_TRAILING_SLASH = False  # Remove trailing slash from routes
SOCIAL_AUTH_AUTH0_KEY = os.environ.get('AUTH0_CLIENT_ID')
SOCIAL_AUTH_AUTH0_SECRET = os.environ.get('AUTH0_CLIENT_SECRET')
SOCIAL_AUTH_AUTH0_SCOPE = [
    'openid',
    'profile',
    'email'
]
SOCIAL_AUTH_AUTH0_DOMAIN = os.environ.get('AUTH0_DOMAIN')
AUDIENCE = None
if os.environ.get('AUTH0_AUDIENCE'):
    AUDIENCE = os.environ.get('AUTH0_AUDIENCE')
else:
    if SOCIAL_AUTH_AUTH0_DOMAIN:
        AUDIENCE = 'https://' + SOCIAL_AUTH_AUTH0_DOMAIN + '/userinfo'
if AUDIENCE:
    SOCIAL_AUTH_AUTH0_AUTH_EXTRA_ARGUMENTS = {'audience': AUDIENCE}
AUTHENTICATION_BACKENDS = {
    'tools.gatekeeper.backends.Auth0',
    'django.contrib.auth.backends.ModelBackend'
}

LOGIN_URL = '/login/auth0'
LOGIN_REDIRECT_URL = '/dashboard'


# ---------------------------------------------------------------------------- #
# HTTPS and Session Settings
# ---------------------------------------------------------------------------- #

# Uncomment if this site supports HTTPS.
# This will cause the login page and other sensitive pages to require HTTPS.
#SSL_ENABLED = True

# Uncomment if using NGINX.
# This will allow Tendenci to properly detect HTTP vs HTTPS client connections
# when using NGINX.  DO NOT use this if Tendenci is not behind NGINX, as that
# will open a security hole.
SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')

# Uncomment these if NGINX is configured to redirect all HTTP connections to
# HTTPS.  This is strongly recommended for live sites.
#SESSION_COOKIE_SECURE = True  # Send Session Cookie over HTTPS only
#CSRF_COOKIE_SECURE = True  # Send CSRF Cookie over HTTPS only

# Depending on configuration, logged in users may either be logged out when the
# user closes their browser, or may remain logged in after the user closes and
# reopens their browser.
# For logins through /admin/login/, SESSION_EXPIRE_AT_BROWSER_CLOSE controls
# this behavior.  (Default is False)
# For logins through /accounts/login/, the "Hide Remember Me" and
# "Remember Me Checked" settings in the "Users" app in Tendenci control this
# behavior, overriding SESSION_EXPIRE_AT_BROWSER_CLOSE.
#SESSION_EXPIRE_AT_BROWSER_CLOSE = True
# Independently of the above behavior, users will also be logged out by both the
# server and their own browser if they do not visit the site for more than
# SESSION_COOKIE_AGE seconds.  However, each page load will reset this counter,
# allowing the user to remain logged in indefinitely as long as they continue to
# visit the site regularly.  (Default is 2 weeks)
#SESSION_COOKIE_AGE = 60*60*24*7*2


# ---------------------------------------------------------------------------- #
# Email Settings
# ---------------------------------------------------------------------------- #


# ---------------------------------------------------------------------------- #
# Payment Gateway Settings
# ---------------------------------------------------------------------------- #


# ---------------------------------------------------------------------------- #
# Cache Settings
# ---------------------------------------------------------------------------- #


# ---------------------------------------------------------------------------- #
# Celery Settings
# ---------------------------------------------------------------------------- #

# Uncomment this setting if you are running the Celery Task System.
#CELERY_IS_ACTIVE = True


# ---------------------------------------------------------------------------- #
# Custom Application Settings
# ---------------------------------------------------------------------------- #

PROJECT_ROOT = os.getcwd()

STATIC_URL = '/static/'

STATIC_ROOT = PROJECT_ROOT + '/static/'

INSTALLED_APPS = lib.modules + \
    tools.modules + \
    [
        # Project imports
        'httpproxy',
        'social_django',
        'address',
        'django_extensions',
        'django_jinja',
        'channels',
        'gunicorn',
        # 'haystack',
        'import_export',
        'simple_history',
        'phonenumber_field',
        'sockpuppet',
        'formtools',
        'dj_pagination',
        'captcha',
        'tastypie',
        'timezone_field',

        # Django libraries
        'django.contrib.admin',
        'django.contrib.auth',
        'django.contrib.contenttypes',
        'django.contrib.sessions',
        'django.contrib.sites',
        'django.contrib.humanize',
        'django.contrib.sitemaps',
        'django.contrib.messages',
        'django.contrib.admindocs',
        'django.contrib.staticfiles',
        'django.contrib.gis',
    ]

DJANGO_HASHIDS_SALT = "itsy bitsy spider"

TEMPLATES = [
    {
        "BACKEND": "django_jinja.backend.Jinja2",
        "APP_DIRS": True,
        "OPTIONS": {
            "match_extension": (".jinja", ".html")
        }
    },
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        "APP_DIRS": True,
        'OPTIONS': {
            'context_processors': [
                'django.contrib.auth.context_processors.auth',
                'django.template.context_processors.debug',
                'django.template.context_processors.i18n',
                'django.template.context_processors.media',
                'django.template.context_processors.request',
                'django.template.context_processors.static',
                'django.contrib.messages.context_processors.messages',
            ],
            'libraries': {
                # Empty for now
            },
            'builtins': [
                # TODO: Look at the value of adding more builtins so that I don't have to explicitly define tags in all of my templates. But do that in the Jinja entry above. ^
                'django.templatetags.i18n',
            ],
        },
        'DIRS': [django_path[0]+'/forms/templates'],
    }
]

STATICFILES_DIRS = [
    # TODO: Change this to be dynamic and/or appropriate to my app.
    "themes/c-street-2020/media"
]

FORM_RENDERER = 'django.forms.renderers.TemplatesSetting'

MIDDLEWARE = [
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.common.CommonMiddleware',
    'dj_pagination.middleware.PaginationMiddleware',
    'django.middleware.locale.LocaleMiddleware',
    'simple_history.middleware.HistoryRequestMiddleware',
]
if os.path.exists(os.path.join(PROJECT_ROOT, 'lib/impersonation/')):
    MIDDLEWARE += ['lib.impersonation.middleware.ImpersonationMiddleware']

# To enable custom URL patterns to be configured in urls.py:
ROOT_URLCONF = 'conf.urls'


# ---------------------------------------------------------------------------- #
# Logging Settings
# ---------------------------------------------------------------------------- #

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'root': {
        'handlers': ['console'],
        'level': 'INFO'
    },
    'handlers': {
        'console': {
            'level': 'INFO',
            'class': 'logging.StreamHandler',
            'formatter': 'simple'
        },
        'sockpuppet': {
          'level': 'DEBUG',
          'class': 'logging.handlers.RotatingFileHandler',
          'filename': 'log/sockpuppet.log',
          'formatter': 'simple'
        }
    },
    'formatters': {
        'simple': {
            'format': '%(asctime)s ⚜️  %(name)s 〉 %(levelname)s 〉 %(message)s'
        },
    },
    'loggers': {
        'sockpuppet': {
            'level': 'DEBUG',
            'handlers': ['sockpuppet']
        }
    }
}
#LOGGING['loggers']['py.warnings'].pop('filters', None)

# To use Sentry (https://docs.sentry.io/):
#SENTRY_DSN = ''
#INSTALLED_APPS += ['raven.contrib.django.raven_compat']
#RAVEN_CONFIG = {'dsn': SENTRY_DSN}


# ---------------------------------------------------------------------------- #
# Haystack Search
# ---------------------------------------------------------------------------- #

HAYSTACK_CONNECTIONS = {
    'default': {
        'ENGINE': 'haystack.backends.whoosh_backend.WhooshEngine',
        'PATH': os.path.join(PROJECT_ROOT, 'whoosh_index', 'main'),
    }
}

HAYSTACK_SEARCH_RESULTS_PER_PAGE = 10

# HAYSTACK_INDEX_LIMITS - row amount to index per core application
# Override for rebuild_index command exists in base core app
HAYSTACK_INDEX_LIMITS = {
    'event_logs': 3000,
}

INDEX_FILE_CONTENT = False
# TODO: This is a dummy setting that doesn't do anything. When I get to setting up Haystack (and Celery, Redis, Solr, etc.).
# https://django-haystack.readthedocs.io/en/master/signal_processors.html
HAYSTACK_SIGNAL_PROCESSOR = 'haystack.signals.BaseSignalProcessor'

# django-sql-explorer
EXPLORER_CONNECTIONS = { 'default': 'default' }
EXPLORER_DEFAULT_CONNECTION = 'default'
EXPLORER_UNSAFE_RENDERING = True
def EXPLORER_PERMISSION_VIEW(u):
    return u.is_superuser
def EXPLORER_PERMISSION_CHANGE(u):
    return u.is_superuser


# ---------------------------------------------------------------------------- #
# Additional Debugging Settings
# ---------------------------------------------------------------------------- #

# Uncomment and configure these settings to enable some additional debugging
# capabilities for clients connecting from one of the specified IPs.
# These debugging capabilities may expose internal/private data, so be careful
# to restrict this appropriately.
# Note that if you are running NGINX, all clients appear to be connecting from
# 127.0.0.1, so this example configuration will give all clients access to these
# debugging capabilities.
# if DEBUG:
#    INTERNAL_IPS = ['127.0.0.1', '::1']

DEBUG_TOOLBAR_ENABLED = False
try:
    import debug_toolbar  # noqa: F401
    MIDDLEWARE += ['debug_toolbar.middleware.DebugToolbarMiddleware']
    INSTALLED_APPS += ['debug_toolbar']
    DEBUG_TOOLBAR_CONFIG = {
        'SHOW_TOOLBAR_CALLBACK': lambda req: DEBUG_TOOLBAR_ENABLED,
        'SHOW_COLLAPSED': False,
    }
except ImportError:
    pass
