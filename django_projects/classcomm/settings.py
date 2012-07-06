# Django settings.py file for classcomm project.

# Instance settings (for debug/prod/testing, etc.)
DEBUG = True
TEMPLATE_DEBUG = True
SITE_ID = 1
INTERNAL_IPS = ('127.0.0.1', '192.168.56.1')
DEBUG_TOOLBAR_CONFIG = {
    'INTERCEPT_REDIRECTS': False,
}

# Admin/Management settings
ADMINS = (
    ('UserName', 'email@email.com')
)
MANAGERS = ADMINS

# Database settings
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'cm2',
        'USER': 'cm2',
        'PASSWORD': 'Sammy2son',
    },
}

# Local time zone for this installation. Choices can be found here:
# http://en.wikipedia.org/wiki/List_of_tz_zones_by_name
# although not all choices may be available on all operating systems.
# If running in a Windows environment this must be set to the same as your
# system time zone.
TIME_ZONE = 'America/Chicago'

# Language code for this installation. All choices can be found here:
# http://www.i18nguy.com/unicode/language-identifiers.html
LANGUAGE_CODE = 'en-us'

# If you set this to False, Django will make some optimizations so as not
# to load the internationalization machinery.
USE_I18N = True

# Root URL file for this django project
ROOT_URLCONF = 'classcomm.urls'

# Absolute path to the directory that holds media.
# Example: "/home/media/media.lawrence.com/"
MEDIA_ROOT = '/var/www/media/'

# URL that handles the media served from MEDIA_ROOT. Make sure to use a
# trailing slash if there is a path component (optional in other cases).
# Examples: "http://media.lawrence.com", "http://example.com/media/"
MEDIA_URL = ''

# URL prefix for admin media -- CSS, JavaScript and images. Make sure to use a
# trailing slash.
# Examples: "http://foo.com/media/", "/media/".
ADMIN_MEDIA_PREFIX = '/media/static/admin/'

# Static Media Root -- All project static files will be stored here.
STATIC_ROOT = '/var/www/media/static/'

# Static URL -- URI prefix for static files.
STATIC_URL = '/media/static/'

# URL for classcomm authentiaction
LOGIN_URL = '/registration/login/'

# Account Activation Window and Automated E-mails
ACCOUNT_ACTIVATION_DAYS = 7
#EMAIL_USE_TLS = 1
#EMAIL_PORT = 436
#EMAIL_HOST_USER = 'accounts@classcomm.geekshack.net'
#EMAIL_HOST_PASSWORD = 'what_it_is'

#### Sentry Configuration (Also see LOGGING) ####
# This should be the absolute URI of sentries store view
#SENTRY_REMOTE_URL = '/sentry/store/'
# Sentry Key--For Securing the Sentry Data Store:
#SENTRY_KEY = '0123456789abcde'
##############################

# Make this unique, and don't share it with anybody.
# Run generate_key.py in the classcomm directory to generate a random key value.
SECRET_KEY = 'r$rh(0u8n&li68^v)eijdi-gvtsk6yqpx#q06j0&gboa1innbu'

# mod_auth_token password
AUTH_TOKEN_PASSWORD = 'JajUpUcilEj4'


# List of Template Context Processors (components typically add context)
TEMPLATE_CONTEXT_PROCESSORS = (
    'django.contrib.auth.context_processors.auth',
    'django.core.context_processors.debug',
    'django.core.context_processors.i18n',
    'django.core.context_processors.media',
    'django.core.context_processors.request',
    'django.core.context_processors.static',
    'django.contrib.messages.context_processors.messages',
)

TEMPLATE_LOADERS = (
    # List of callables that know how to import templates from the various sources.
    # Here we are wrapping out two loaders with a cached loader for performance optimization.
    ('django.template.loaders.cached.Loader', (
        'django.template.loaders.filesystem.Loader',
        'django.template.loaders.app_directories.Loader',
    )),
)

TEMPLATE_DIRS = (
    # List of known template locations (additional to the known sources)
    # Put strings here, like "/home/html/django_templates" or "C:/www/django/templates".
    # Always use forward slashes, even on Windows.
    # Don't forget to use absolute paths, not relative paths.
    '/var/django_templates/',
)

MIDDLEWARE_CLASSES = (
    'django.middleware.gzip.GZipMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'debug_toolbar.middleware.DebugToolbarMiddleware',
#    'django.middleware.transaction.TransactionMiddleware',
)

INSTALLED_APPS = (
    'django.contrib.contenttypes',
    'django.contrib.staticfiles',
    'django.contrib.auth',
    'django.contrib.messages',
    'django.contrib.sessions',
    'django.contrib.sites',
    'django.contrib.admin',
    'django.contrib.admindocs',
    'classcomm.student_portal',
    'classcomm.instructor_portal',
    'classcomm.registration',
    'classcomm.dashboard',
    'debug_toolbar',
    'south',
#    'paging',
#    'indexer', # Sentry Depend.
#    'paging', # Sentry Depend.
#    'overseer',
#    'sentry',
#    'sentry.client',
)

# Configure Project Logging using Django Logging setting and specifying
# Dict-Config to Python 1.6
LOGGING = {
    'version': 1,
    'formatters': {
        'simple': {
            'format': '%(asctime)s %(levelname)s %(module)s [%(name)s] - %(message)s \n',
        },
        'verbose': {
            'format': '%(asctime)s %(levelname)s %(module)s %(process)d %(thread)d %(message)s'
        },
    },
    'handlers': {
        'log_test': {
            'class': 'logging.handlers.TimedRotatingFileHandler',
            'filename': '/var/log/classcomm/log-test.log',
            'when': 'H',
            'interval': 1,
            'backupCount': 5,
            'formatter': 'simple',
        },
        'classcomm': {
            'class': 'logging.handlers.TimedRotatingFileHandler',
            'filename': '/var/log/classcomm/classcomm.log',
            'when': 'H',
            'interval': 1,
            'backupCount': 5,
            'formatter': 'verbose',
        },
        'student_portal': {
            'class': 'logging.FileHandler',
            'filename': '/var/log/classcomm/student_portal.log',
            'mode': 'a',
            'formatter': 'verbose',
        },
        'instructor_portal': {
            'class': 'logging.FileHandler',
            'filename': '/var/log/classcomm/instructor_portal.log',
            'mode': 'a',
            'formatter': 'verbose',
        },
        'django': {
            'class': 'logging.FileHandler',
            'filename': '/var/log/classcomm/django.log',
            'mode': 'a',
            'formatter': 'verbose',
        },
        'django_sql': {
            'class': 'logging.FileHandler',
            'filename': '/var/log/classcomm/django-sql.log',
            'mode': 'a',
            'formatter': 'verbose',
        },
#        'sentry_handler': {
#            'class': 'sentry.client.handlers.SentryHandler',
#            'formatter': 'verbose',
#        },
#        'stream_handler': {
#            'class': 'logging.StreamHandler',
#            'formatter': 'verbose',
#        }
    },
    # Root logger (complete logging)
    'root' : { 'level' : 'WARNING', 'handlers' : ['classcomm'], #, 'sentry_handler'],
    },
    'loggers': {
        'log_test': { 'level': 'INFO', 'handlers': ['log_test'] },
        'student_portal': { 'level': 'INFO', 'handlers': ['student_portal'] },
        'instructor_portal': { 'level': 'INFO', 'handlers': ['instructor_portal'] },
        'django': { 'handlers': ['django'] },
        'django.core.urlresolvers': { 'level': 'DEBUG' },
        'django.core.handlers.base': { 'level': 'DEBUG' },
        'django.db.models.loading': { 'level': 'DEBUG' },
        'django.db.backends.util': { 'level': 'DEBUG',
                                     'propagate': False,
                                     'handlers': ['django_sql'] },
        # 'sentry.errors': { 'level': 'INFO', 'handlers': ['stream_handler'] },
    },
}


#### Classcomm Application Settings ####

#### Shared Global ####

# Global offset for minutes after Due Date to accept Submission On-Time (Implements a short cushion of leniency)
ALLOW_LATE_SUBMISSION_MINUTES = 20

# Django Paginator Settings -- # of Items Per Page (Default values)
PAGINATOR_NUM_ASSIGNMENTS = 5
PAGINATOR_NUM_ENROLLMENTS = 20


#### Registration Settings ####

# Display Open Registrations sub-system
REGISTRATION_OPEN = True


#### Student_Portal Specific ####

# Display a link to Courses Listed with Open_Enrollments (Not Implemented)
OPEN_ENROLLMENTS = True

