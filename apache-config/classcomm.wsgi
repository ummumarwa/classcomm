import os, sys

sys.path.append('/var/django_projects/')
os.environ['DJANGO_SETTINGS_MODULE'] = 'classcomm.settings'

path = '/var/django_projects/classcomm'
if path not in sys.path:
    sys.path.append(path)
import django.core.handlers.wsgi
application = django.core.handlers.wsgi.WSGIHandler()
