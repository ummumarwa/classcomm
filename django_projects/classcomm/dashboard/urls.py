"""
URLConf for classcomm dashboard application.

If the default behavior of these views is acceptable to you, simply
use a line like this in your root URLconf to set up the default URLs
for registration::

    (r'^/', include('dashboard.urls')),

"""


from django.conf.urls.defaults import *


# urlpatterns for classcomm.student_portal
urlpatterns = patterns('',
    # Dashboard Panels
    (r'^$', 'dashboard.views.index'),
    (r'^index.html$', 'dashboard.views.index'),
    (r'^welcome/$', 'dashboard.views.index'),

    # AJAX Calls
    (r'^server-time/$', 'dashboard.ajax.server_time'),
)

