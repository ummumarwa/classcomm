from django import template         # Template related functionality for registering as a template tag library
from django.conf import settings    # Get Project Settings
import datetime                     # Date related functionality


# Mark this a valid Django template library
register = template.Library()

@register.filter
def adjustDateWeeks(date, weeks):
    """ Adjust @param date forward by the number of @param weeks. """
    return date + datetime.timedelta(weeks=weeks)
# End Def

@register.filter
def adjustDateDays(date, days):
    """ Adjust @param date forward by the number of @param days. """
    return date + datetime.timedelta(days=days)
# End Def

@register.filter
def subtractDateMinutes(date, minutes):
    """ Adjust @param date forward by the number of @param days. """
    return date - datetime.timedelta(minutes=minutes)
# End Def

@register.filter
def isLateNow(dueDate):
    """
    Check if the current server datetime has passed the @param dueDate.
    This function applies the ALLOW_LATE_SUBMISSION_MINUTES setting globally.

    """
    return subtractDateMinutes(dueDate.today(), settings.ALLOW_LATE_SUBMISSION_MINUTES) > dueDate
# End Def


@register.filter
def isNaturallyLateNow(dueDate):
    """ Check if the current server datetime has passed the @param dueDate. """
    return dueDate.today() > dueDate
# End Def

@register.filter
def isLate(dueDate, theDate):
    """
    Check if @param theDate has passed @param dueDate
    This function applies the ALLOW_LATE_SUBMISSION_MINUTES setting globally.
    
    """
    return subtractDateMinutes(theDate, settings.ALLOW_LATE_SUBMISSION_MINUTES) > dueDate
# End Def

@register.filter
def isNaturallyLate(dueDate, theDate):
    """ Check if @param theDate has passed @param dueDate """
    return theDate > dueDate
# End Def

@register.filter
def printUser(user):
    """ Construct html output of @parame User. """
    if (user.first_name and user.last_name):
        result = user.first_name + " " + user.last_name
    else:
        result = user.username
    result += " - "
    if user.email:
        result += '(<a href="mailto:' + user.email + '">' + user.email + '</a>)'
    else:
        result += '<i>(Unlisted E-mail)</i>'
    return result
# End Def

@register.filter
def getTrClass(assignmentData):
    """ Discover which css tr styling to apply to the current assignment. """
    if assignmentData[2]:
        return '"assignmentGraded"'
    if assignmentData[1]:
        return '"assignmentSubmitted"'
    return '"assignmentNormal"'
# End Def

@register.filter
def printSubmitFormStart(assignmentId):
    """ Construct html output for the start of @param SubmissionForm. """
    # Start form
    result = '\n<form action="assignments.html" method="post" enctype="multipart/form-data">\n'

    # Store the assignment id
    result += "<div style='display:none'>"
    result += '<input type="hidden" name="assignment" value="'
    result += str(assignmentId)
    result += '" /></div>\n'
    return result
# End Def

@register.filter
def printSubmitFormEnd(form):
    """ Construct html output for the end of @param SubmissionForm. """
    # Apply the file upload field
    #result = '<div>' + str(form['file']) + '<br /><br /></div>\n'
    result = '<div><input type="file" name="file" class="id_file" /><br /><br /></div>'

    # Finalize the Form
    result += '<div><input type="submit" value="Submit" /></div>\n'
    result += '</form>\n'
    return result
# End Def

