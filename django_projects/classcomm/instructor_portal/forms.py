from classcomm.student_portal.models import *
from django import forms


class AnnouncementForm(forms.ModelForm):
    """ Form for posting new Announcement to classcomm. """

    class Meta:
        # Base the form off the model Submission
        model = Announcement
        # We will fill these in automatically
        exclude = ('department', 'course')
# End Def

class AssignmentForm(forms.ModelForm):
    """ Form for creating new course Assignment. """

    class Meta:
        # Base form off the model Assignment
        model = Assignment
        # We will fill these in automatically
        exclude = ('make_global', 'department', 'course', 'pub_date')
# End Def

class GradeForm(forms.ModelForm):
    """ Form for returning new Grade. """

    class Meta:
        # Base form off the model Grade
        model = Grade
        # We will fill these in automatically
        exclude = ('enrollment', 'assignment')
# End Def

class InformationForm(forms.ModelForm):
    """ Form for creating new Information. """

    class Meta:
        # Base form off the model Information
        model = Information
        # We will fill these in automatically
        exclude = ('department', 'course')
# End Def

class ResourceForm(forms.ModelForm):
    """ Form for creating new Information. """

    class Meta:
        # Base form off the model Information
        model = Resource
        # We will fill these in automatically
        exclude = ('department', 'course')
# End Def

class DueDateOverrideForm(forms.ModelForm):
    """ Form for creating new DueDateOverride. """

    class Meta:
        # Base form off the model DueDateOverride
        model = DueDateOverride
        # We will fill these in automatically
        exclude = ('enrollment', 'assignment')
# End Def
