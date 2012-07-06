from django.http import HttpResponse
from django.utils import simplejson as json

from classcomm.student_portal.models import *


def enrollment_assignments(request, enrollment_id):
    """ AJAX call to get JSON list of Assignments for enrollment_id.
    """

    if request.is_ajax(): # Fetch Assignment List
        enrollment = Enrollment.objects.get(id__exact=enrollment_id)
        assignments = Assignment.objects.values('pk', 'name').filter(course=enrollment.course).order_by('name')
        payload = json.dumps([a for a in assignments])
    else:
        payload = "Sorry, this URL is for AJAX calls only."
    return HttpResponse(payload, content_type = 'application/javascript; charset=utf8')
# End Def

def department_courses(request, department_id):
    """ AJAX call to get JSON list of Courses for department_id.
    """

    if request.is_ajax(): # Fetch Assignment List
        department = Department.objects.get(id__exact=department_id)
        courses = Course.objects.values('pk', 'name').filter(department=department).order_by('name')
        payload = json.dumps([c for c in courses])
    else:
        payload = "Sorry, this URL is for AJAX calls only."
    return HttpResponse(payload, content_type = 'application/javascript; charset=utf8')
# End Def

