"""
Root URLConf for classcomm Django project.


"""
from django.conf.urls.defaults import *

# Next two lines are needed to enable the django-admin:
from django.contrib import admin
admin.autodiscover()


urlpatterns = patterns('',
    # Root Dashboard
    (r'', include('dashboard.urls')),

    # For student portal (formerly named handin):
    (r'^student/', include('student_portal.urls')),
    
    # Deprecated but lets keep handin links working for a little while ...
    (r'^handin/', include('student_portal.urls')),
    
    # For instructor portal:
    (r'^instructor/', include('instructor_portal.urls')),

    # For User Authentication and Registration URLs:
    (r'^registration/', include('registration.backends.default.urls')),

    # For Overseer
    (r'^status', include('overseer.urls', namespace='overseer')),
    
    # For Sentry
    # (r'^sentry/', include('sentry.urls')),

    # Uncomment the next two lines to enable the admin-docs and the admin itself:
    (r'^admin/doc/', include('django.contrib.admindocs.urls')),
    (r'^admin/', include(admin.site.urls)),
)
