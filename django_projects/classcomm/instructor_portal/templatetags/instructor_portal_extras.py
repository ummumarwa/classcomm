# Template related functionality
from django import template
# For our application permissions
from classcomm.instructor_portal import views

# Mark this a valid Django template library
register = template.Library()

@register.filter
def daysPassed(theDate):
    """ Return the number of days that have passed since the parameter date. """
    timedelta = theDate.today() - theDate
    return timedelta.days
# End Def

@register.filter
def checkscriptTrClass(age):
    """
    Returns CSS class name for a Submission in checkscript based on @param age (int days).

    """
    result = 'class="'
    if age > 7:
        result += 'old'
    elif age > 2:
        result += 'ok'
    else:
        result += 'recent'
    result += '"'
    return result
# EndDef

@register.filter
def printUsername(user):
    """ Construct html output for the @param User. """
    if user.email:
        result = '<a href="mailto:' + user.email + '">' + user.username + '</a>'
        return result
    else:
        return user.username
    return result
# EndDef

####
# Permissions Related Filters (typically used to displaying admin/edit links to correct users)
####

@register.filter
def editAnnouncement(access_type):
    """ Returns True or False if @param access_type flag can add/edit Announcements. """
    if access_type in [views.COURSE_DIRECTOR, views.COURSE_INSTRUCTOR, views.COURSE_MENTOR]:
        return True
    else:
        return False
# EndDef

@register.filter
def editAssignment(access_type):
    """ Returns True or False if @param access_type flag can add/edit Assignments. """
    if access_type in [views.COURSE_DIRECTOR, views.COURSE_INSTRUCTOR]:
        return True
    else:
        return False
# EndDef

@register.filter
def editInformation(access_type):
    """ Returns True or False if @param access_type flag can add/edit Information. """
    if access_type in [views.COURSE_DIRECTOR, views.COURSE_INSTRUCTOR]:
        return True
    else:
        return False
# EndDef

@register.filter
def editResource(access_type):
    """ Returns True or False if @param access_type flag can add/edit Resource. """
    if access_type in [views.COURSE_DIRECTOR, views.COURSE_INSTRUCTOR]:
        return True
    else:
        return False
# EndDef

@register.filter
def editEnrollment(access_type):
    """ Returns True or False if @param access_flag can add/edit Enrollment. """
    if access_type in [views.COURSE_DIRECTOR, views.COURSE_INSTRUCTOR]:
        return True
    else:
        return False
# EndDef

@register.filter
def editInstructor(access_type):
    """ Returns True or False if @param access_flag can add/edit Instructor. """
    if access_type in [views.COURSE_DIRECTOR]:
        return True
    else:
        return False
# EndDef

@register.filter
def editMentor(access_type):
    """ Returns True or False if @param access_flag can add/edit Mentor. """
    if access_type in [views.COURSE_DIRECTOR, views.COURSE_INSTRUCTOR]:
        return True
    else:
        return False
# EndDef

@register.filter
def editExtraCredit(access_type):
    """ Returns True or False if @param access_flag can add/edit ExtraCredit. """
    if access_type in [views.COURSE_DIRECTOR, views.COURSE_INSTRUCTOR, views.COURSE_MENTOR]:
        return True
    else:
        return False
# EndDef

