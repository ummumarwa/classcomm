import logging
logger = logging.getLogger('student_portal')

from django.core.urlresolvers import reverse
from django.core.exceptions import ObjectDoesNotExist
from django.core.paginator import Paginator, InvalidPage, EmptyPage
from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.admin.models import LogEntry, ADDITION
from django.contrib.contenttypes.models import ContentType
from django.utils.encoding import force_unicode
from django.db.models import Q
from django.http import HttpResponse
from django.http import HttpResponseRedirect
from django.template import RequestContext, loader

from classcomm.student_portal.forms import *
from classcomm.student_portal.models import *
from classcomm.student_portal.templatetags.student_portal_extras import *

@login_required
def index(request):
    """
    Main classcomm student portal view for students to see welcome page
    dynamically linking them into their enrolled courses.

    """
    # Get all enrollments for the current user
    enrollments = Enrollment.objects.all().filter(student=request.user).select_related().order_by('course')

    # Get all global announcements ordered by date
    announcements = Announcement.objects.all().filter(make_global=1).select_related('author').order_by('-pub_date')

    # Specify template, generate context, and return response
    template = loader.get_template('student_portal/index.html')
    context = RequestContext(request, {"enrollments": enrollments, "announcements": announcements})
    return HttpResponse(template.render(context))
# End Def

@login_required
def open_enrollments(request):
    """
    open enrollments view for Students discovering and enrolling in Courses.
    Present Behavior: Any Course with open_enrollments flag set in which the
    student does not have an existing enrollment.

    """
    if request.POST: # Handle POST data
        course = Course.objects.get(id__exact=request.POST['course'])
        if course.open_enrollments: # Verify Course allows open_enrollments
            # Verify request.user does not have existing Course Enrollment
            if not Enrollment.objects.all().filter(student=request.user).filter(course=course):

                # Finally create and save new user enrollment, return to Open Enrollments
                enrollment = Enrollment(student=request.user, course_id=request.POST['course'],
                    start_date=datetime.date.today().isoformat())
                enrollment.save()
                messages.success(request, "Now Enrolled in " + course.name)
                LogEntry.objects.log_action(request.user.pk, ContentType.objects.get_for_model(enrollment).pk,
                                            enrollment.pk, force_unicode(enrollment), action_flag=ADDITION)
                return HttpResponseRedirect(reverse('student_portal.views.open_enrollments', args=[]))
    # EndPOST

    # Get all enrollments and courses for the current user
    enrollments = Enrollment.objects.all().filter(student=request.user).select_related().order_by('-course')
    courses = Course.objects.all().filter(open_enrollments=1).select_related()

    # Exclude listing any courses where User already has Enrollment
    course_list = []
    for course in courses:
        add_course = 1
        for enrollment in enrollments:
            if course == enrollment.course:
                add_course = 0
        if add_course:
            course_list.append(course)

    # Specify template, generate context, and return response
    template = loader.get_template('student_portal/open_enrollments.html')
    context = RequestContext(request, {"courses": course_list})
    return HttpResponse(template.render(context))
# End Def

@login_required
def course_index(request, enrollment_id):
    """
    Course welcome view where students view announcements,
    details about their selected Course (based on enrollment_id), as well as
    an expanded course menu for assignments, resources and information, etc.

    """
    # Verify enrollment access and create default blocking behavior
    enrollment = Enrollment.objects.select_related('student', 'mentor', 'course',
                                            'course__director', 'course__department').get(id__exact=enrollment_id)
    course = enrollment.course # get handle to Enrollment's Course
    enrollment_access = verify_enrollment(request.user, enrollment)
    template = loader.get_template('student_portal/course_blocked.html')
    context = RequestContext(request, {"enrollment": enrollment, "access_flag": enrollment_access})
    if enrollment_access == ENROLLMENT_ACTIVE:

        # Find all Instructors, Mentors and Announcements for this Course
        instructors = Instructor.objects.all().filter(course=course).select_related('instructor')
        mentors = Mentor.objects.all().filter(course=course).select_related('mentor')
        announcements = Announcement.objects.all().filter(Q(course=course) |
                                                          Q(department=course.department)
                                                          ).select_related('author').order_by('-pub_date')

        # Set correct template; Create context; Render Response 
        template = loader.get_template('student_portal/course_index.html')
        context = RequestContext(request, {"course": course, "instructors": instructors, "mentors": mentors,
           "enrollment": enrollment, "announcements": announcements})
    return HttpResponse(template.render(context))
# End Def

@login_required
def course_assignments(request, enrollment_id):
    """
    Student assignments view for the course of a particular enrollment.
    Authenticates enrollment for request.user, processes any POST data
    as a submission form with due date logic and redundancy check,
    gathers and arranges assignment data as a list of tuples:
    (Assignment, Submission, Grade, DueDateOverride) for the template to process.
    Protects Submissions against CSRF attacks using {% csrf_token %}.
    
    """
    # Verify enrollment access and create default blocking behavior
    enrollment = Enrollment.objects.select_related().get(id__exact=enrollment_id)
    enrollment_status = verify_enrollment(request.user, enrollment)
    template = loader.get_template('student_portal/course_blocked.html')
    context = RequestContext(request, {"enrollment": enrollment, "access_flag": enrollment_status})
    if enrollment_status == ENROLLMENT_ACTIVE:

        if request.POST: # When POST data, process Assignment Submission
            assignment = Assignment.objects.get(id__exact=request.POST['assignment'])
            allow_late = assignment.allow_late # Custom flag for allowing late handin (default: Assignment.allow_late)
            submissions = Submission.objects.all().filter(enrollment=enrollment.id).filter(assignment=assignment.id)
            if not submissions: # Verify no existing Enrollment/Assignment Submission
                is_late = False
                try: # First Check for DueDateOverride
                    dueDate = DueDateOverride.objects.filter(enrollment=enrollment.id).filter(assignment=assignment.id)[0]
                    is_late = isLateNow( adjustDateDays( adjustDateWeeks(enrollment.start_date, dueDate.weeks_after),
                                                        dueDate.days_after))
                    allow_late = dueDate.allow_late # When DueDateOverride use that flag value.
                except IndexError: # Otherwise Apply Default Assignment Due Date
                    if assignment.apply_due_date:
                        is_late = isLateNow( adjustDateDays( adjustDateWeeks(enrollment.start_date,
                                                            assignment.weeks_after), assignment.days_after))
                # Create and save Submission when on_time or allow_late 
                if not is_late or allow_late:
                    instance = Submission(enrollment=enrollment, assignment=assignment, on_time=(not is_late))
                    newSubmission = SubmissionForm(request.POST, request.FILES, instance=instance)
                    newSubmission.save()
                    messages.success(request, "Success: New HW Submission created for " + assignment.name + "!")
                    LogEntry.objects.log_action(request.user.pk, ContentType.objects.get_for_model(instance).pk,
                                            instance.pk, force_unicode(instance), action_flag=ADDITION)
                else: # Otherwise report errors
                    messages.error(request, "Failure: Late Submissions not allowed for " + assignment.name + "!")
            else: # Other
                messages.error(request, "Failure: Existing HW Submission for " + assignment.name + "!")
        # End POST

        # Find all Assignments, Grades, Submissions and DueDateOverrides
        course = enrollment.course
        assignments = Assignment.objects.all().filter(course=course.id).order_by('name')
        grades = Grade.objects.all().filter(enrollment=enrollment.id)
        submissions = Submission.objects.all().filter(enrollment=enrollment.id)
        dueDateOverrides = DueDateOverride.objects.all().filter(enrollment=enrollment.id)

        # Create a list of tuples for easy template widget generation cycle
        # Each Tuple:(Assignment, Submission, Grade, DueDateOverride)
        assignment_data = list() # For Each Assignment:
        for assignment in assignments:
            currentSubmission = None # Find the Submission
            for submission in submissions:
                if submission.assignment_id == assignment.id:
                    currentSubmission = submission
                    break
            currentGrade = None # Find the Grade
            for grade in grades:
                if grade.assignment_id == assignment.id:
                    currentGrade = grade
                    break
            currentDDO = None # Find the DueDateOverride
            for dueDateOverride in dueDateOverrides:
                if dueDateOverride.assignment_id == assignment.id:
                    currentDDO = dueDateOverride
                    break
            # Add the Assignment tuple to the data list
            assignment_data.append((assignment, currentSubmission, 
                currentGrade, currentDDO))

        # Tuck data into a Django Paginator keep page view organization more clean and scalable.
        paginator = Paginator(assignment_data, settings.PAGINATOR_NUM_ASSIGNMENTS)
        try: # Page request must be an int--If not, deliver first page.
            page = int(request.GET.get('page', '1'))
        except ValueError:
            page = 1
        try: # If page request is out of range, deliver last page of results.
            current_page = paginator.page(page)
        except (EmptyPage, InvalidPage):
            current_page = paginator.page(paginator.num_pages)

        # Set template, and Create Context
        template = loader.get_template('student_portal/course_assignments.html')
        context = RequestContext(request, {"course": course, "form": SubmissionForm(),
            "enrollment": enrollment, "assignment_list": current_page})
    # Return page view
    return HttpResponse( template.render(context) )
# End Def

@login_required
def delete_submission(request, enrollment_id, submission_id):
    """
    Delete an Assignment Submission with @param Submission so long as
    it matches @param Submission (for Security).

    """
    # Verify Enrollment Access and create default blocking behavior
    enrollment = Enrollment.objects.select_related().get(id__exact=enrollment_id)
    enrollment_status = verify_enrollment(request.user, enrollment)
    template = loader.get_template('student_portal/course_blocked.html')
    context = RequestContext(request, {"enrollment": enrollment, "access_flag": enrollment_status})
    if enrollment_status == ENROLLMENT_ACTIVE: # verify requested Enrollment

        if request.POST: # Process Submission Delete request when POST
            try: # Request Submission from URL parameters
                submission = Submission.objects.select_related().get(id__exact=submission_id)
            except ObjectDoesNotExist: # Return to the course assignments
                return HttpResponseRedirect(reverse('student_portal.views.course_assignments', args=[enrollment.id,]))
        
            # Verify @param Submission.Enrollment corresponds to the @param Enrollment
            if submission.enrollment == enrollment:

                # Verify Submission has not yet been assigned Grade:
                delete_submission = False
                grade = Grade.objects.all().filter(enrollment=enrollment.id).filter(assignment=submission.assignment.id)
                if not grade:
                    delete_submission = True
                else:
                    messages.error(request, 'Delete Submission Failure: Submission already has Grade!')

                # Now verify Submission is not past any kind of Due Date
                try: # First check for DueDateOverride
                    dueDate = DueDateOverride.objects.filter(enrollment=enrollment.id).filter(assignment=submission.assignment.id)[0]
                    delete_submission = not isLateNow(adjustDateDays(adjustDateWeeks(enrollment.start_date,
                                                                                     dueDate.weeks_after),
                                                dueDate.days_after))
                except IndexError: # Otherwise check for Assignment global Due Date
                    assignment = submission.assignment
                    if assignment.apply_due_date:
                        delete_submission = not isLateNow(adjustDateDays(adjustDateWeeks(enrollment.start_date,
                                                                                         assignment.weeks_after),
                                                    assignment.days_after))
                # Delete Submission when eligible:
                if delete_submission:
                    submission.delete()
                    messages.success(request, 'Success: Submission Deleted for Assignment ' + assignment.name + '!')
                elif not grade:
                    messages.error(request, 'Delete Submission Failure: Assignment already is past due!')
            else:
                messages.error(request, 'Delete Submission Failure: Bad Submission <--> Enrollment request!')
        else:
            messages.error(request, 'Delete Submission Failure: No POST data!')
    else: # Return Course Blocked view when Enrollment not Active
        return HttpResponse( template.render(context) )

    # Return Redirect to the course assignments view page
    return HttpResponseRedirect(reverse('student_portal.views.course_assignments', args=[enrollment.id,]))
# End Def

@login_required
def course_resources(request, enrollment_id):
    """
    Main student view for listing the department and course resources populated in the DB.
    
    """
    # Verify enrollment access and create default blocking behavior
    enrollment = Enrollment.objects.select_related().get(id__exact=enrollment_id)
    enrollment_status = verify_enrollment(request.user, enrollment)
    template = loader.get_template('student_portal/course_blocked.html')
    context = RequestContext(request, {"enrollment": enrollment, "access_flag": enrollment_status})
    if enrollment_status == ENROLLMENT_ACTIVE:

        # Get the course
        course = enrollment.course

        # Get the resources for the requested course
        course_resources = Resource.objects.all().filter(course=course.id).order_by('name')

        # Get the resources for the requested department
        department_resources = Resource.objects.all().filter(department=course.department.id).order_by('name')

        # Set template; Create context
        template = loader.get_template('student_portal/course_resources.html')
        context = RequestContext(request, {"course": course, 
            "enrollment": enrollment, "course_resources": course_resources, 
            "department_resources": department_resources})

    # Return page view response
    return HttpResponse( template.render(context) )
# End Def

@login_required
def course_info(request, enrollment_id):
    """
    Main student view for listing the department and course information
    populated in the DB with links to each individual complete info view: course_info_view
    
    """
    # Verify enrollment access and create default blocking behavior
    enrollment = Enrollment.objects.select_related().get(id__exact=enrollment_id)
    enrollment_status = verify_enrollment(request.user, enrollment)
    template = loader.get_template('student_portal/course_blocked.html')
    context = RequestContext(request, {"enrollment": enrollment, "access_flag": enrollment_status})
    if enrollment_status == ENROLLMENT_ACTIVE:

        # Get the information, set template, create context
        course = enrollment.course
        course_infos = Information.objects.all().filter(course=course.id).order_by('name')
        department_infos = Information.objects.all().filter(department=(course.department.id)).order_by('name')
        template = loader.get_template('student_portal/course_information.html')
        context = RequestContext(request, {"course": course,
           "enrollment": enrollment, "course_infos": course_infos,
           "department_infos": department_infos} )

    # Return page view response
    return HttpResponse( template.render(context) )
# End Def

@login_required
def course_info_view(request, enrollment_id, info_id):
    """
    Main student view for listing the specific course information 
    of @param Info when granted by @param Enrollment for the request user.

    """
    # Verify enrollment access and create default blocking behavior
    enrollment = Enrollment.objects.select_related().get(id__exact=enrollment_id)
    enrollment_status = verify_enrollment(request.user, enrollment)
    template = loader.get_template('student_portal/course_blocked.html')
    context = RequestContext(request, {"enrollment": enrollment, "access_flag": enrollment_status})
    if enrollment_status == ENROLLMENT_ACTIVE:

        # Get the information, template and create context
        info = Information.objects.get(id__exact=info_id)
        template = loader.get_template('student_portal/course_info_view.html')
        context = RequestContext(request, {"course": enrollment.course,
           "enrollment": enrollment, "info": info} )

    # Return page view response
    return HttpResponse( template.render(context) )
# End Def


#################################################
# BEGIN PERMISSIONS HELPER FUNCTIONS
#################################################

#################################################
# Enrollment permissions flags for the request.user:
# Change the course_blocked.html template needs corresponding values are updated!
ENROLLMENT_ACTIVE = 1
ENROLLMENT_BAD_USER = -1
ENROLLMENT_DISABLED = 0
ENROLLMENT_EARLY = 3
ENROLLMENT_ENDED = 4
#################################################
def verify_enrollment(user, enrollment):
    """ Returns a permissions flag matching for @param user using the @param Enrollment.
    Recommended Usage is to pass request.user and one of that user's Enrollments.

    """
    # Verify current user matches @param Enrollment object
    if enrollment.student == user:

        # First handle any access_mode overrides
        if enrollment.access_mode == 'Active':
            return ENROLLMENT_ACTIVE
        if enrollment.access_mode == 'Disabled':
            return ENROLLMENT_DISABLED

        # Otherwise, has Enrollment period begun?
        if enrollment.start_date > datetime.date.today():
            return ENROLLMENT_EARLY

        # It has begun: Finally, determine Enrollment hasn't expired
        if enrollment.length_override:
            if adjustDateWeeks(enrollment.start_date, enrollment.length_override) > datetime.date.today():
                return ENROLLMENT_ACTIVE
            else:
                return ENROLLMENT_ENDED
        else: # Use Default Course.length
            if adjustDateWeeks(enrollment.start_date, enrollment.course.enrollment_length) > datetime.date.today():
                return ENROLLMENT_ACTIVE
            else:
                return ENROLLMENT_ENDED
    # EndIf -- Now Return Failure
    return ENROLLMENT_BAD_USER
# End Def


