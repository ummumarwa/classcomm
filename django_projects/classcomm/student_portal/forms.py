from classcomm.student_portal.models import *
from django import forms


class SubmissionForm(forms.ModelForm):
    """
    Form for submitting work/creating Submission
    
    """
    class Meta:
        # Base the form off the model Submission
        model = Submission
        # We will fill these in automatically
        exclude = ('enrollment','assignment','on_time')   
# End Def
