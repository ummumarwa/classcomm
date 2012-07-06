"""
URLConf for student portal classcomm application.

If the default behavior of these views is acceptable to you, simply
use a line like this in your root URLconf to set up the default URLs
for registration::

    (r'^student/', include('student_portal.urls')),
    
"""

from django.conf.urls.defaults import *


# urlpatterns for classcomm.student_portal
urlpatterns = patterns('',
   (r'^$', 'student_portal.views.index'),
   (r'^index.html$', 'student_portal.views.index'),
   (r'^welcome/$', 'student_portal.views.index'),
   (r'^open_enrollments/$',
        'student_portal.views.open_enrollments'),
   (r'^courseindex/(\d{1,5})/$', 
        'student_portal.views.course_index'),
   (r'^courseindex/(\d{1,5})/index.html$', 
        'student_portal.views.course_index'),
   (r'^courseindex/(\d{1,5})/assignments.html$', 
        'student_portal.views.course_assignments'),
   (r'^courseindex/(\d{1,5})/delsubmission/(\d{1,5})/$', 
        'student_portal.views.delete_submission'),
   (r'^courseindex/(\d{1,5})/resources.html$', 
        'student_portal.views.course_resources'),
   (r'^courseindex/(\d{1,5})/information.html$', 
        'student_portal.views.course_info'),
   (r'^courseindex/(\d{1,5})/infoview/(\d{1,5})/$', 
        'student_portal.views.course_info_view'),
   # Custom AJAX method for specialized admin templates for dynamic filtering
   (r'^assignments-eid/(\d{1,5})/$',
        'student_portal.ajax.enrollment_assignments'),
)
