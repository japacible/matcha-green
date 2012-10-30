import os
import dj_database_url

SECRET_KEY = '*r-$b*8hglm+959&7x043hlm6-&6-3d3vfc4((7yd0dbrakhvi'

if (os.getenv('SERVER_SOFTWARE', '').startswith('Google App Engine') or os.getenv('SETTINGS_MODE') == 'prod'):
  DATABASES = {
    'default': {
      'ENGINE': 'google.appengine.ext.django.backends.rdbms',
      'INSTANCE': 'sjf-northwest:sjf',
      'NAME': 'sjf_devel',
    }
  }
  DEBUG = False
else:
  DATABASES = {
    'default': {
      'ENGINE': 'django.db.backends.mysql',
      'USER': 'root',
      'PASSWORD': 'SJFdb',
      'HOST': 'localhost',
      'NAME': 'sjfdb',
    }
  }
  DATABASES['default'] = dj_database_url.config()
  DEBUG = True

INSTALLED_APPS = (
  'django.contrib.admin',
  'django.contrib.contenttypes',
  'django.contrib.auth',
  'django.contrib.sessions',
  'django.contrib.messages',
  'grants',
  'fund',
  'djangoappengine', # last so it can override a few manage.py commands
)

MIDDLEWARE_CLASSES = (
  'google.appengine.ext.appstats.recording.AppStatsDjangoMiddleware', #must be first
  'django.middleware.common.CommonMiddleware',
  'django.contrib.sessions.middleware.SessionMiddleware',
  'django.contrib.auth.middleware.AuthenticationMiddleware',
  'django.contrib.messages.middleware.MessageMiddleware',
  'fund.middleware.MembershipMiddleware',
)

TEMPLATE_CONTEXT_PROCESSORS = (
  'django.contrib.auth.context_processors.auth',
  'django.core.context_processors.request',
  'django.core.context_processors.media',
  'django.contrib.messages.context_processors.messages',
)

TEMPLATE_DIRS = (os.path.join(os.path.dirname(__file__), 'templates'),)

ROOT_URLCONF = 'urls'

LOGGING = {
  'version': 1,
}

#djangoappengine email settings
EMAIL_BACKEND = 'djangoappengine.mail.AsyncEmailBackend'
EMAIL_QUEUE_NAME = 'default'

STATIC_URL = '/static/'

USE_TZ = True
TIME_ZONE = 'America/Los_Angeles'

#settings to try to make error reporting happen
SERVER_EMAIL = 'sjfnwads@gmail.com'
DEFAULT_FROM_EMAIL = 'sjfnwads@gmail.com'
ADMINS = (('Aisa', 'sjfnwads@gmail.com'),)

DEFAULT_FILE_STORAGE = 'djangoappengine.storage.BlobstoreStorage'
SERVE_FILE_BACKEND = 'djangoappengine.storage.serve_file'

#FILE_UPLOAD_HANDLERS = (
    #'grants.views.AppUploadHandler', #custom attempt
#    'djangoappengine.storage.BlobstoreFileUploadHandler',
#  )

### CUSTOM SETTINGS

APP_SUPPORT_EMAIL = 'webmaster@socialjusticefund.org' #just email
APP_SEND_EMAIL = 'sjfnwads@gmail.com' #can include name
SUPPORT_FORM_URL = 'https://docs.google.com/spreadsheet/viewform?formkey=dHZ2cllsc044U2dDQkx1b2s4TExzWUE6MQ'
APP_BASE_URL = 'http://sjf-nw.appspot.com/' #until i learn how to do this the real way..
