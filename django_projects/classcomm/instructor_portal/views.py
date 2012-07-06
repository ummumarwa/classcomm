import logging
logger = logging.getLogger('instructor_portal')

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
from django.db.models import Sum
from django.http import HttpResponse, HttpResponseRedirect, Http404
from django.template import RequestContext, loader

from classcomm.student_portal.models import *
from classcomm.instructor_portal.forms import *

@login_required
def index(request):
    """
    Main classcomm instructor portal view for instructors, mentors,
    course directors and Department directors to see
    a welcome page that dynamically links them to their allowed actions.
    
    """
    # Get all Courses where request.user is Director, Instructor, Mentor or Mentor_Assigned
    user = request.user
    courses = Course.objects.all().filter(Q(director=user) |
        Q(instructor__instructor=user) | Q(enrollment__mentor=user) |
        Q(enrollment__course__mentor__mentor=user)).distinct().select_related('department', 'director').order_by('name')
    instructors = Instructor.objects.all().filter(instructor=user).select_related('course', 'course__department')
    mentors = Mentor.objects.all().filter(mentor=user).select_related('course', 'course__department')
    mentor_assigns = Enrollment.objects.all().filter(mentor=user).select_related('course', 'course__department',
                                                                    'student').order_by('student__username')
    # Create Dictionary of Course Tuples for easy template cycle
    # Tuple:(Course, Department, Roles, Mentor Assigns)
    course_data = dict()
    for course in courses: # Add All Courses to Dictionary
        if course.director == user:
            course_data[course.id] = (course, course.department, ['Director'], [])
        else:
            course_data[course.id] = (course, course.department, [], [])
    # Fill out remaining User Roles
    for instructor in instructors: # Add Instructor Roles
        course = instructor.course
        if not course_data.has_key(course.id): # (add Course if it doesn't exist)
            course_data[course.id] = (course, course.department, ['Instructor',], [])
        if not 'Instructor' in course_data[course.id][2]:
            course_data[course.id][2].append('Instructor')
    for mentor in mentors: # Add Mentor Roles
        course = mentor.course
        if not course_data.has_key(course.id): # (add a Course if it doesn't exist)
            course_data[course.id] = (course, course.department, ['Mentor',], [])
        if not 'Mentor' in course_data[course.id][2]:
            course_data[course.id][2].append('Mentor')
    for mentor_assign in mentor_assigns: # Add Mentor Assign Roles
        course = mentor_assign.course
        if not course_data.has_key(course.id): # (add a Course if it doesn't exist)
            course_data[course.id] = (course, course.department, ['Mentor_ASN',], [])
        if not 'Mentor_ASN' in course_data[course.id][2]:
            course_data[course.id][2].append('Mentor_ASN')
    # Fill out Mentor Assigned Students
    for enrollment in mentor_assigns:
        course = enrollment.course
        if not course_data.has_key(course.id): # (add a Course if it doesn't exist)
            course_data[course.id] = (course, course.department, [], [])
        if not enrollment.student in course_data[course.id][3]:
            course_data[course.id][3].append(enrollment.student)

    # Get all global announcements ordered by date
    announcements = Announcement.objects.all().filter(make_global=1).select_related('author').order_by('-pub_date')

    # Specify template, generate context, and return response
    template = loader.get_template('instructor_portal/index.html')
    context = RequestContext(request, {"course_data": course_data, "announcements": announcements})
    return HttpResponse(template.render(context))
# End Def

@login_required
def course_index(request, course_id):
    """
    Course welcome view for instructors to see announcements,
    details about selected course as well as
    an expanded course menu for assignments, resources and information.
    
    """
    try: # Try to get Course and raise 404 if it doesn't exist.
        course = Course.objects.select_related('department', 'director').get(id__exact=course_id)
    except Course.DoesNotExist:
        raise Http404
    access_type = verify_course(request.user, course) # Verify access with default blocking behavior
    template = loader.get_template('instructor_portal/course_blocked.html')
    context = RequestContext(request, {"access_flag": access_type})
    if access_type in [COURSE_DIRECTOR, COURSE_INSTRUCTOR, COURSE_MENTOR, COURSE_MENTOR_LIMIT]:

        # Find all Instructors, Mentors and Announcements for this Course
        instructors = Instructor.objects.all().filter(course=course).select_related('instructor')
        mentors = Mentor.objects.all().filter(course=course).select_related('mentor')
        student_assigns = Enrollment.objects.all().filter(mentor=request.user).select_related('student')
        announcements = Announcement.objects.all().filter(Q(course=course) |
                                                          Q(department=course.department)
                                                          ).select_related('author').order_by('-pub_date')
        # Set template; Create Context; Return page view
        template = loader.get_template('instructor_portal/course_index.html')
        context = RequestContext(request, {"access_type": access_type,"course": course,  "instructors": instructors,
            "mentors": mentors, "student_assigns":  student_assigns, "announcements": announcements})
    return HttpResponse(template.render(context))
# End Def

@login_required
def course_announcement_add(request, course_id):
    """
    Instructor announcements view for adding an Announcement to a particular Course.
    Authenticates for request.user, processes any POST data
    as an AnnouncementForm and effectively adds the Announcement to the database
    and redirects to course_index or returns to course_announcement_add
    with appropriate error messages.
    Protects submissions against CSRF attacks using {% csrf_token %}.
    
    """
    # Verify access with default blocking behavior
    course = Course.objects.select_related().get(id__exact=course_id)
    access_type = verify_course(request.user, course)
    template = loader.get_template('instructor_portal/course_blocked.html')
    context = RequestContext(request, {"access_flag": access_type})
    if access_type in [COURSE_DIRECTOR, COURSE_INSTRUCTOR, COURSE_MENTOR]:
    
        form = AnnouncementForm()
        if request.POST:
            # Create and save Announcement when form passes validation
            instance = Announcement(make_global=False, course_id=course.id)
            form = AnnouncementForm(request.POST, instance=instance)
            if form.is_valid():
                form.save()
                messages.success(request, 'Announcement successfully added to Course!')
                LogEntry.objects.log_action(request.user.pk, ContentType.objects.get_for_model(instance).pk,
                                            instance.pk, force_unicode(instance), action_flag=ADDITION)
                return HttpResponseRedirect(reverse(
                    'instructor_portal.views.course_index', args=[course.id,]))

        # Finally Set template, create Context and return Response
        template = loader.get_template('instructor_portal/course_announcement_add.html')
        context = RequestContext(request, {"course": course,"form": form})
    return HttpResponse( template.render(context) )
# End Def

@login_required
def course_announcement_delete(request, course_id, announcement_id):
    """
    Delete an Announcement with @param Announcement so long
    as it is in Course with @param Course.

    """
    try: # Verify Course @param with 404 block page error
        course = Course.objects.select_related().get(id__exact=course_id)
    except Course.DoesNotExist:
        raise Http404
    access_type = verify_course(request.user, course)
    if access_type in [COURSE_DIRECTOR, COURSE_INSTRUCTOR, COURSE_MENTOR]:
        if request.POST:
            try: # Grab Announcement from URL parameters
                announcement = Announcement.objects.select_related().get(id__exact=announcement_id)
            except ObjectDoesNotExist: # Add warning message and forward to the Course index
                messages.warning(request, 'Announcement Delete Failure: No matching Announcement found!')
                return HttpResponseRedirect(reverse(
                    'instructor_portal.views.course_index', args=[course_id,]))
            # Verify Announcement corresponds to the verified Course
            if (announcement.department == course.department) or (announcement.course == course):
                announcement.delete()
                messages.success(request, 'Announcement successfully deleted from Course!')
            else:
                messages.warning(request, 'Announcement Delete Failure: Invalid URL Parameters!')
    return HttpResponseRedirect(reverse('instructor_portal.views.course_index', args=[course_id,]))
# End Def

@login_required
def course_assignments(request, course_id):
    """
    Instructor Assignments view for a particular Course.
    Authenticates access for request.user, link to Assignment Add
    gathers and arranges assignment data as a list of tuples:
    (Assignment, Submission, Grade, DueDateOverride) for the template.
    
    """
    # Verify access with default blocking behavior
    course = Course.objects.select_related().get(id__exact=course_id)
    access_type = verify_course(request.user, course)
    template = loader.get_template('instructor_portal/course_blocked.html')
    context = RequestContext(request, {"access_flag": access_type})
    if access_type in [COURSE_DIRECTOR, COURSE_INSTRUCTOR, COURSE_MENTOR, COURSE_MENTOR_LIMIT]:

        # Find all Assignments, Grades, Submissions and DueDateOverrides
        assignments = Assignment.objects.all().filter(course=course.id).order_by('name')

        # Tuck data into a Django Paginator (which will means extra total page views +Queries)
        paginator = Paginator(assignments, settings.PAGINATOR_NUM_ASSIGNMENTS)
        try: # Page request must be an int--If not, deliver first page.
            page = int(request.GET.get('page', '1'))
        except ValueError:
            page = 1
        try: # If page request is out of range, deliver last page of results.
            current_page = paginator.page(page)
        except (EmptyPage, InvalidPage):
            current_page = paginator.page(paginator.num_pages)

        # Set template, and create Context
        template = loader.get_template('instructor_portal/course_assignments.html')
        context = RequestContext(request, {"access_type": access_type, "course": course, "assignments": current_page})
    return HttpResponse( template.render(context) )
# End Def

@login_required
def assignment_add(request, course_id):
    """
    Instructor assignments view for adding an assignment to a particular Course.
    Authenticates for request.user, processes any POST data as an AssignmentForm,
    and effectively adds the assignment to the database redirecting to course_assignments, 
    or returns to assignment_add with form errors.
    Protects submissions against CSFR attacks using {% csrf_token %}.
    
    """
    # Verify access with default blocking behavior
    course = Course.objects.select_related().get(id__exact=course_id)
    access_type = verify_course(request.user, course)
    template = loader.get_template('instructor_portal/course_blocked.html')
    context = RequestContext(request, {"access_flag": access_type})
    if access_type in [COURSE_DIRECTOR, COURSE_INSTRUCTOR]:
    
        # Process POST given POST data
        form = AssignmentForm()
        if request.POST:
            # Create and save Assignment when form passes validation
            instance = Assignment(course_id=course.id)
            form = AssignmentForm(request.POST, request.FILES, instance=instance)
            if form.is_valid():
                form.save()
                messages.success(request, "Assignment " + instance.name + " added to Course " + course.name)
                LogEntry.objects.log_action(request.user.pk, ContentType.objects.get_for_model(instance).pk,
                                            instance.pk, force_unicode(instance), action_flag=ADDITION)
                return HttpResponseRedirect(reverse('instructor_portal.views.course_assignments', args=(course.id,)))

        # Set template, create Context and Return page view
        template = loader.get_template('instructor_portal/course_assignment_add.html')
        context = RequestContext(request, {"course": course, "form": form})
    return HttpResponse( template.render(context) )
# End View

@login_required
def course_information(request, course_id):
    """
    Instructor Course View for listing Course and Department Resources
    with @param Course and corresponding Department.

    """
    # Verify access with default blocking behavior
    course = Course.objects.select_related().get(id__exact=course_id)
    access_type = verify_course(request.user, course)
    template = loader.get_template('instructor_portal/course_blocked.html')
    context = RequestContext(request, {"access_flag": access_type})
    if access_type in [COURSE_DIRECTOR, COURSE_INSTRUCTOR, COURSE_MENTOR, COURSE_MENTOR_LIMIT]:

        # Get the requested Course/Department Information
        course_information = Information.objects.all().filter(course=course.id).order_by('name')
        department_information = Information.objects.all().filter(department=course.department.id).order_by('name')

        # Set template; Create context
        template = loader.get_template('instructor_portal/course_information.html')
        context = RequestContext(request, {"access_type": access_type, "course": course,
            "course_infos": course_information, "department_infos": department_information})
    # Return page view response
    return HttpResponse( template.render(context) )
# End View

@login_required
def course_resources(request, course_id):
    """
    Instructor Course View for listing Course and Department Resources
    with @param Course and corresponding Department.

    """
    # Verify access with default blocking behavior
    course = Course.objects.select_related().get(id__exact=course_id)
    access_type = verify_course(request.user, course)
    template = loader.get_template('instructor_portal/course_blocked.html')
    context = RequestContext(request, {"access_flag": access_type})
    if access_type in [COURSE_DIRECTOR, COURSE_INSTRUCTOR, COURSE_MENTOR, COURSE_MENTOR_LIMIT]:

        # Get the requested Course/Department Resources
        course_resources = Resource.objects.all().filter(course=course).order_by('name')
        department_resources = Resource.objects.all().filter(department=course.department).order_by('name')

        # Set template; Create context
        template = loader.get_template('instructor_portal/course_resources.html')
        context = RequestContext(request, {"access_type": access_type, "course": course,
            "course_resources": course_resources, "department_resources": department_resources})
    # Return page view response
    return HttpResponse( template.render(context) )
# EndView

@login_required
def checkscript_all(request):
    """
    Script for finding which homework sets (Submissions) have not yet been graded
    based on the access permissions of the current user.
    Unfortunately this is one area that is tricky and requires several queries
    at our desired data.

    """
    if request.user.is_superuser: # Get all checkscript submissions for super users
        courses = Course.objects.all().select_related('department')
        submissions = Submission.objects.all().select_related().filter(add_checkscript=True).order_by('date')
        # Add message; Set template; Create Context; Return Page View.
        messages.success(request, 'Now Showing: Complete Checkscript Listing!')
        template = loader.get_template('instructor_portal/checkscript.html')
        context = RequestContext(request, {'courses': courses, 'submissions': submissions})
        return HttpResponse(template.render(context))
    else: # Otherwise redirect to the default checkscript View with warning message
        messages.warning(request, "Checkscript/All only works for super users!  " +
                         "Default checkscript shows all content related to your classcomm roles.")
        return HttpResponseRedirect(reverse('instructor_portal.views.checkscript', args=[]))
# EndView

@login_required
def checkscript(request):
    """
    Script for finding which homework sets (Submissions) have not yet been graded
    based on the access permissions of the current user.
    Unfortunately this is one area that is tricky and requires several queries
    at our desired data.

    """
    # This is one of the most complex and beautiful query refactors in classcomm thus far!
    courses = Course.objects.all().filter(Q(director=request.user) |
            Q(instructor__instructor=request.user) |
            Q(enrollment__mentor=request.user) |
            Q(enrollment__course__mentor__mentor=request.user)).distinct()
    submissions = Submission.objects.all().filter(add_checkscript=True).filter(
            Q(enrollment__course__director=request.user) |
            Q(enrollment__course__instructor__instructor=request.user) |
            Q(enrollment__mentor=request.user) |
            Q(enrollment__course__mentor__mentor=request.user)
        ).distinct().select_related('assignment', 'assignment__course', 'assignment__course__department',
                                    'enrollment', 'enrollment__student', 'enrollment__mentor' ).order_by('date')
    # Add Message; Set template; Create Context; Return page view
    messages.success(request, 'Now Showing: Checkscript Listings for Your User Roles!')
    template = loader.get_template('instructor_portal/checkscript.html')
    context = RequestContext(request, {'courses': courses, 'submissions': submissions})
    return HttpResponse(template.render(context))
# EndView

@login_required
def checkscript_course(request, course_id):
    """
    Script for finding which homework sets have not yet been graded
    based on the access permissions of the current user.

    """
    try: # Verify Course @param with 404 block page error
        course = Course.objects.select_related().get(id__exact=course_id)
    except Course.DoesNotExist:
        raise Http404
    courses = Course.objects.all().filter(Q(director=request.user) |
            Q(instructor__instructor=request.user) |
            Q(enrollment__mentor=request.user) |
            Q(enrollment__course__mentor__mentor=request.user)).distinct()
    submissions = Submission.objects.all().filter(add_checkscript=True).filter(enrollment__course=course).filter(
            Q(enrollment__course__director=request.user) |
            Q(enrollment__course__instructor__instructor=request.user) |
            Q(enrollment__mentor=request.user) |
            Q(enrollment__course__mentor__mentor=request.user)
        ).distinct().select_related('assignment', 'assignment__course', 'assignment__course__department',
                                    'enrollment', 'enrollment__student', 'enrollment__mentor' ).order_by('date')
    # Add Message; Set template; Create context; Return page view
    messages.success(request, "Now Showing: Checkscript Listing for your role in Course " + course.name + "!")
    template = loader.get_template('instructor_portal/checkscript.html')
    context = RequestContext(request, {'courses': courses, 'submissions': submissions})
    return HttpResponse(template.render(context))
# EndView

@login_required
def roster_tools(request, course_id):
    """ Instructor view for course roster with links to student grade reports/actions. """
    
    # Verify access with default blocking behavior
    course = Course.objects.select_related().get(id__exact=course_id)
    access_type = verify_course(request.user, course)
    template = loader.get_template('instructor_portal/course_blocked.html')
    context = RequestContext(request, {"access_flag": access_type})
    if access_type in [COURSE_DIRECTOR, COURSE_INSTRUCTOR, COURSE_MENTOR,
        COURSE_MENTOR_LIMIT]:

        # Find all enrollments for this course
        enrollments = Enrollment.objects.all().filter(course=course.id).select_related().order_by()

        # Tuck data into a Paginator which will means extra total page views =>
        # more SQL queries, sorting, and thus processing overhead. However
        # it will keep page view organization more clean and scalable.
        paginator = Paginator(enrollments, settings.PAGINATOR_NUM_ENROLLMENTS)
        try: # Page request must be an int--If not, deliver first page.
            page = int(request.GET.get('page', '1'))
        except ValueError:
            page = 1
        try: # If page request is out of range, deliver last page of results.
            current_page = paginator.page(page)
        except (EmptyPage, InvalidPage):
            current_page = paginator.page(paginator.num_pages)

        # Set template; Create Context
        template = loader.get_template('instructor_portal/course_roster.html')
        context = RequestContext(request, {"course": course,
            "access_type": access_type,
            "enrollments": current_page})
    # Return page view
    return HttpResponse(template.render(context))
# EndView

@login_required
def grade_report(request, course_id, enrollment_id):
    """ Main view for an Enrollment Grade Report. """
    
    # Verify access with default blocking behavior
    enrollment = Enrollment.objects.select_related().get(id__exact=enrollment_id)
    course = Course.objects.select_related().get(id=course_id)
    template = loader.get_template('instructor_portal/course_blocked.html')
    context = RequestContext(request, {})
    if enrollment.course.id == course.id: # Verify URL Correctness
        access_type = verify_course(request.user, course)
        context = RequestContext(request, {"access_flag": access_type})
        if access_type in [COURSE_DIRECTOR, COURSE_INSTRUCTOR, COURSE_MENTOR, COURSE_MENTOR_LIMIT]:

            # Find all Assignments and related data for this Course/Enrollment
            assignments = Assignment.objects.all().filter(course=course.id).order_by('name')
            grades = Grade.objects.all().filter(enrollment=enrollment.id)
            submissions = Submission.objects.all().filter(enrollment=enrollment.id)
            dueDateOverrides = DueDateOverride.objects.all().filter(enrollment=enrollment.id)
            extra_credit = ExtraCredit.objects.all().filter(enrollment=enrollment.id)

            # Create list of Tuples for easy template cycle
            # Tuple:(Assignment, Submission, Grade, DueDateOverride)
            assignment_data = list()
            for assignment in assignments:
                # Find the submission
                currentSubmission = None
                for submission in submissions:
                    if submission.assignment_id == assignment.id:
                        currentSubmission = submission
                        break
                # Find the grade
                currentGrade = None
                for grade in grades:
                    if grade.assignment_id == assignment.id:
                        currentGrade = grade
                        break
                # Find any associated DueDateOverride
                currentDDO = None
                for dueDateOverride in dueDateOverrides:
                    if dueDateOverride.assignment_id == assignment.id:
                        currentDDO = dueDateOverride
                        break
                # Add the tuple to a list
                assignment_data.append((assignment, currentSubmission, currentGrade, currentDDO))
            # EndFor

            # Compute Aggregate Values for the context now also
            points_earned = grades.aggregate(Sum('points_earned'))
            points_possible = assignments.aggregate(Sum('points_possible'))
            points_extra_credit = extra_credit.aggregate(Sum('points_earned'))
            point_summary = (points_earned, points_possible, points_extra_credit)

            # Tuck data into a Paginator which will means extra total page views =>
            # more SQL queries, sorting, and thus processing overhead. However
            # it will keep page view organization more clean and scalable.
            paginator = Paginator(assignment_data, settings.PAGINATOR_NUM_ASSIGNMENTS)
            try: # Page request must be an int--If not, deliver first page.
                page = int(request.GET.get('page', '1'))
            except ValueError:
                page = 1
            try: # If page request is out of range, deliver last page of results.
                current_page = paginator.page(page)
            except (EmptyPage, InvalidPage):
                current_page = paginator.page(paginator.num_pages)

            # Set template; Create Context
            template = loader.get_template('instructor_portal/grade_report.html')
            context = RequestContext(request, {"access_type": access_type, "course": course, "enrollment": enrollment,
                "point_summary": point_summary, "assignment_list": current_page, "extra_credit": extra_credit})
    else:
        messages.error(request, "Grade Report Error: Invalid URL parameters!")
    return HttpResponse(template.render(context))
# EndView

@login_required
def return_grade(request, enrollment_id, assignment_id):
    """
    Instructor checkscript view for returning a Grade for a particular Assignment/Enrollment.
    Authenticates for request.user, processes any POST data using appropriate ModelForm,
     and effectively adds the Announcement to the database.
    Redirects to course_index or returns to course_announcement_add with appropriate error messages.
    Protects adding Grade against CSRF attacks using {% csrf_token %}.

    """
    # Verify access with default blocking behavior
    enrollment = Enrollment.objects.select_related().get(id__exact=enrollment_id)
    assignment = Assignment.objects.select_related().get(id__exact=assignment_id)
    if enrollment.course == assignment.course: # Parameter URL must be correctly formed
        access_type = verify_course(request.user, enrollment.course)
        if access_type in [COURSE_DIRECTOR, COURSE_INSTRUCTOR, COURSE_MENTOR, COURSE_MENTOR_LIMIT]:
            
            form = GradeForm()
            if request.POST: # When POST: Create Grade and save obj when form passes validation
                instance = Grade(enrollment_id=enrollment.id, assignment_id=assignment.id)
                form = GradeForm(request.POST, request.FILES, instance=instance)
                if form.is_valid():
                    form.save()
                    messages.success(request, 'New Grade returned for Assignment: ' + assignment.name)
                    LogEntry.objects.log_action(request.user.pk, ContentType.objects.get_for_model(instance).pk,
                                                instance.pk, force_unicode(instance), action_flag=ADDITION)
                    return HttpResponseRedirect(reverse('instructor_portal.views.grade_report',
                                                        args=[assignment.course.id, enrollment.id,]))
        else:
            # Return Action Blocked if not authorized user
            template = loader.get_template('instructor_portal/course_blocked.html')
            context = RequestContext(request, {"access_flag": access_type})
            return HttpResponse( template.render(context) )
    else:
        messages.warning(request, "return_grade: Invalid URL parameters!")

    # Set template, and create Context and Return page view
    template = loader.get_template('instructor_portal/student_grade_return.html')
    context = RequestContext(request, {"form": form,
        "enrollment": enrollment,
        "course": enrollment.course,
        "assignment": assignment})
    return HttpResponse( template.render(context) )
# EndView

@login_required
def delete_grade(request, course_id, enrollment_id, grade_id):
    """ Delete Grade with @param Grade so long as it is a valid request.

    """
    # Verify access with default blocking behavior
    course = Course.objects.select_related().get(id__exact=course_id)
    access_type = verify_course(request.user, course)
    if access_type in [COURSE_DIRECTOR, COURSE_INSTRUCTOR, COURSE_MENTOR]:

        if request.POST: # POST: Grab Grade from URL parameters
            try:
                grade = Grade.objects.select_related().get(id__exact=grade_id)
            except ObjectDoesNotExist: # Return to grade_report with warning
                messages.warning(request, 'Grade with grade_id ' + grade_id + 'not found!')
                return HttpResponseRedirect(reverse( 'instructor_portal.views.grade_report',
                                                     args=[course_id, enrollment_id,]))
            # Verify Grade corresponds to Verified Course
            if grade.assignment.course == course:
                messages.success(request, 'Deleted Grade for Assignment: ' + grade.assignment.name)
                grade.delete()
    # Redirect to the course Assignments view
    return HttpResponseRedirect(reverse('instructor_portal.views.grade_report', args=[course_id, enrollment_id,]))
# End Def

@login_required
def add_DDO(request, enrollment_id, assignment_id):
    """
    Instructor checkscript view for adding a DueDateOverride for a particular Assignment/Enrollment.
    Authenticates for request.user, processes any POST data as an Form,
     and effectively adds the Announcement to the database.
    Redirects to course_index or returns to course_announcement_add with appropriate error messages.
    Protects adding DueDateOverride against CSRF attacks using {% csrf_token %}.

    """
    # Verify access with default blocking behavior
    enrollment = Enrollment.objects.select_related().get(id__exact=enrollment_id)
    assignment = Assignment.objects.select_related().get(id__exact=assignment_id)
    if enrollment.course == assignment.course: # Parameter URL must also be formed correctly
        access_type = verify_course(request.user, enrollment.course)
        if access_type in [COURSE_DIRECTOR, COURSE_INSTRUCTOR, COURSE_MENTOR, COURSE_MENTOR_LIMIT]:

            form = DueDateOverrideForm()
            if request.POST: # When POST: Create and save Grade if form passes validation
                instance = DueDateOverride(enrollment_id=enrollment.id, assignment_id=assignment.id)
                form = DueDateOverrideForm(request.POST, request.FILES, instance=instance)
                if form.is_valid():
                    form.save()
                    messages.success(request, 'New Due Date Override added for Assignment ' + assignment.name)
                    LogEntry.objects.log_action(request.user.pk, ContentType.objects.get_for_model(instance).pk,
                                                instance.pk, force_unicode(instance), ADDITION)
                    return HttpResponseRedirect(reverse('instructor_portal.views.grade_report',
                                                        args=[assignment.course.id, enrollment.id,]))
        else:
            # Return Action Blocked if not authorized user
            template = loader.get_template('instructor_portal/course_blocked.html')
            context = RequestContext(request, {"access_flag": access_type})
            return HttpResponse( template.render(context) )
    else:
        messages.warning(request, "Unable to add Due Date Override: Invalid URL parameters!")
    # Set template, and create Context and Return page view
    template = loader.get_template('instructor_portal/student_DDO_add.html')
    context = RequestContext(request, {"form": form,
        "enrollment": enrollment,
        "course": enrollment.course,
        "assignment": assignment})
    return HttpResponse( template.render(context) )
# EndView

@login_required
def delete_DDO(request, course_id, enrollment_id, DDO_id):
    """ Delete a DueDateOverride with @param DDO_id for valid requests.

    """
    # Verify access with default blocking behavior
    course = Course.objects.select_related().get(id__exact=course_id)
    access_type = verify_course(request.user, course)
    if access_type in [COURSE_DIRECTOR, COURSE_INSTRUCTOR, COURSE_MENTOR]:

        if request.POST:
            try: # Grab DueDateOverride from URL parameters
                DDO = DueDateOverride.objects.select_related().get(id__exact=DDO_id)
            except ObjectDoesNotExist:
                # Return to the Course index
                messages.warning(request, 'Unable to Delete Due Date Override: Invalid DDO_id in parameter URL!')
                return HttpResponseRedirect(reverse('instructor_portal.views.grade_report',
                                                    args=[course_id, enrollment_id,]))
            # Verify DueDateOverride corresponds to the verified Course
            if DDO.assignment.course == course:
                messages.success(request, 'Due Date Override removed from Assignment: ' + DDO.assignment.name)
                DDO.delete()
    # Return Redirect to the course assignments view page
    return HttpResponseRedirect(reverse('instructor_portal.views.grade_report', args=[course_id, enrollment_id,]))
# EndView


#################################################
# BEGIN PERMISSIONS HELPER FUNCTIONS
#################################################

#################################################
# Permissions Flags for the request.user:
# When these values change, they correspondingly need to
# be adjusted in the course_blocked.html template.
COURSE_BAD_USER = -1
COURSE_DIRECTOR = 2
COURSE_INSTRUCTOR = 3
COURSE_MENTOR = 4
COURSE_MENTOR_LIMIT = 5
DEPT_DIRECTOR = 6 # New (Unimplemented) User type.
#################################################


def verify_course(user, course):
    """
    Returns one of the above permission flags that determines if the @param user
      (which should be request.user) has access level in relation to the @param Course object.

    """
    # Check if user is COURSE_DIRECTOR
    if course.director == user:
        return COURSE_DIRECTOR
        
    # Check if user is COURSE_INSTRUCTOR
    instructors = Instructor.objects.all().select_related().filter(course=course).filter(instructor=user)
    for instructor in instructors:
        if instructor.course == course:
            return COURSE_INSTRUCTOR
        
    # Check if user is COURSE_MENTOR
    mentors = Mentor.objects.all().select_related().filter(course=course).filter(mentor=user)
    for mentor in mentors:
        if mentor.course == course:
            return COURSE_MENTOR
    
    # Check if user is COURSE_MENTOR_LIMIT
    enrollment_assigns = Enrollment.objects.all().filter(mentor=user).filter(course=course)
    for enrollment in enrollment_assigns:
        if enrollment.course == course:
            return COURSE_MENTOR_LIMIT

    # User does not verify course, return COURSE_BAD_USER
    return COURSE_BAD_USER
# End Def


def verify_enrollment(user, enrollment):
    """
    Returns one of the above permission flags that determines if the @param user
      (which should be request.user) has access level in relation to the @param Enrollment object.

    """
    # Check if user is COURSE_DIRECTOR
    if enrollment.course.director == user:
        return COURSE_DIRECTOR

    # Check if user is COURSE_INSTRUCTOR
    instructors = Instructor.objects.all().select_related().filter(course=enrollment.course).filter(instructor=user)
    for instructor in instructors:
        if instructor.course == course:
            return COURSE_INSTRUCTOR

    # Check if user is COURSE_MENTOR
    mentors = Mentor.objects.all().select_related().filter(course=course).filter(mentor=user)
    for mentor in mentors:
        if mentor.course == course:
            return COURSE_MENTOR

    # Check if user is COURSE_MENTOR_LIMIT
    enrollment_assigns = Enrollment.objects.all().filter(mentor=user).filter(course=course)
    for enrollment in enrollment_assigns:
        if enrollment.course == course:
            return COURSE_MENTOR_LIMIT

    # User does not verify course, return COURSE_BAD_USER
    return COURSE_BAD_USER
# End Def

