from .base import *

SECRET_KEY = 'dev-key'

DEBUG = True
TEMPLATE_DEBUG = True
ALLOWED_HOSTS = ['*']

SITE_URL = 'http://localhost:8000'

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'dev-db.sqlite3'),
    }
}

MIDDLEWARE_CLASSES += ('ajaxerrors.middleware.ShowAJAXErrors',)
