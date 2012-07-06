"""
URLConf for student portal classcomm application.

If the default behavior of these views is acceptable to you, simply
use a line like this in your root URLconf to set up the default URLs
for registration::

    (r'^instructor/', include('instructor_portal.urls')),
"""

from django.conf.urls.defaults import *


# urlpatterns for classcomm.instructor_portal
urlpatterns = patterns('',
    # Introduction
    (r'^$', 'instructor_portal.views.index'),
    (r'^index.html$', 'instructor_portal.views.index'),
    (r'^welcome/$', 'instructor_portal.views.index'),
    # Announcements
    (r'^courseindex/(\d{1,5})/$',
        'instructor_portal.views.course_index'),
    (r'^courseindex/(\d{1,5})/announcement/add/$',
        'instructor_portal.views.course_announcement_add'),
    (r'^courseindex/(\d{1,5})/announcement/delete/(\d{1,5})/$',
        'instructor_portal.views.course_announcement_delete'),
    # Assignments
    (r'^courseindex/(\d{1,5})/assignments/$',
        'instructor_portal.views.course_assignments'),
    (r'^courseindex/(\d{1,5})/assignments/add/$',
        'instructor_portal.views.assignment_add'),
    # Information
    (r'^courseindex/(\d{1,5})/information/$',
        'instructor_portal.views.course_information'),    
    # Resources
    (r'^courseindex/(\d{1,5})/resources/$',
        'instructor_portal.views.course_resources'),
    # Checkscript
    (r'^checkscript/$', 'instructor_portal.views.checkscript'),
    (r'^checkscript/all/$', 'instructor_portal.views.checkscript_all'),
    (r'^checkscript/course/(\d{1,5})/$',
        'instructor_portal.views.checkscript_course'),
    # Roster Tools
    (r'^courseindex/(\d{1,5})/roster_tools/$',
        'instructor_portal.views.roster_tools'),
    (r'^courseindex/(\d{1,5})/roster_tools/grade_report/(\d{1,5})/$',
        'instructor_portal.views.grade_report'),
    (r'^roster_tools/(\d{1,5})/return/grade/(\d{1,5})/$',
        'instructor_portal.views.return_grade'),
    (r'^courseindex/(\d{1,5})/roster_tools/grade_report/(\d{1,5})/delete/grade/(\d{1,5})/$',
        'instructor_portal.views.delete_grade'),
    (r'^roster_tools/(\d{1,5})/grade_report/addDDO/(\d{1,5})/$',
        'instructor_portal.views.add_DDO'),
    (r'^courseindex/(\d{1,5})/roster_tools/(\d{1,5})/deleteDDO/(\d{1,5})/$',
        'instructor_portal.views.delete_DDO'),
)

