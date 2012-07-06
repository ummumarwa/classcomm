from django.db import models
from django.contrib.auth.models import User, Group
from classcomm.student_portal.fields import ProtectedFileField
from django.core.exceptions import ObjectDoesNotExist, ValidationError, NON_FIELD_ERRORS

from datetime import datetime
import os

""" This file (models.py) defines the Database Schema for the core classcomm object types.
    ALWAYS call model.full_clean() OR form.is_valid() to protect Database from radical DB entries!!!
    Calling model.full_clean() OR form.is_valid() calls 3 underlying methods (clean, clean_fields, validate_unique)

    * We no longer make duplicate checks in save()--in order to optimize the overall number of queries!
    ** On production hosts, Allow only code that follows this best practice to be executed!
    *** Avoid using the command line to interact with models on production hosts!

"""


class Department(models.Model):
    """ Data-Model representing a Department in Classcomm. """

    # Data Model (DB) Fields
    name = models.CharField(max_length=150)

    def __unicode__(self):
        """ Default unicode string describing the Department. (comment omitted elsewhere in file). """
        return self.name

    def validate_unique(self, exclude=None):
        """ Verifies Department is unique or raises ValidationError. """
        if self.name:
            departments = Department.objects.all().filter(name=self.name)
            for department in departments:
                if department.pk != self.pk:
                    error_msg = 'Already existing Department with name ' + self.name + '!'
                    raise ValidationError({NON_FIELD_ERRORS: [error_msg]})
        super(Department, self).validate_unique()
    # EndDef
# EndClass

class Course(models.Model):
    """ Data Model representing a Course in Classcomm.
        All Courses are contained by a Department and requires both name and description.
        Additionally, all Courses must specify a default Enrollment length (in weeks).
        Optionally, a Course may specify a single Course Director User.
        Also Optionally, a Course may be marked as available for open_enrollments (default=False).
    """

    # Data Model (DB) Fields
    department = models.ForeignKey(Department)
    name = models.CharField(max_length=100)
    director = models.ForeignKey(User, verbose_name='Course Director', null=True, blank=True)
    enrollment_length = models.IntegerField('Default Enrollment Length (in Weeks)', default=16)
    description = models.TextField('Description')
    open_enrollments = models.BooleanField("Open Student Enrollments?", default=False)

    def __unicode__(self):
        return (self.name)
    
    def validate_unique(self, exclude=None):
        """ Verifies Course is unique (may raise ValidationError when not). """
        if self.department and self.name:
            courses = Course.objects.all().filter(department=self.department).filter(name=self.name)
            for course in courses:
                if course.pk != self.pk:
                    error_msg = 'Existing Course ' + self.name + ' in Department ' + self.department.name + '!'
                    raise ValidationError({NON_FIELD_ERRORS: [error_msg]})
        super(Course, self).validate_unique()

    def delete(self):
        """ Consider removing User from Director Group on Delete. """
        try:
            if Course.objects.all().filter(director=self.director).count() <= 1:
                director_group = Group.objects.get(name="Director")
                self.director.groups.remove(director_group)
        except ObjectDoesNotExist:
            pass
        super(Course, self).delete()

    def save(self):
        """ Add User to admin and Instructor Group on save (if not already). """
        if not self.director.is_staff:
            self.director.is_staff = True
            self.director.save()
        try:
            if self.director.groups.all().filter(name="Director").count() == 0:
                director_group = Group.objects.get(name="Director")
                self.director.groups.add(director_group)
        except ObjectDoesNotExist:
            pass
        super(Course, self).save()
# EndClass

class Instructor(models.Model):
    """ Data Model binding a User as an Instructor to Course object.
        Any Course can now have multiple Instructors.
        Course object additionally allows an optional Course Director User to be specified.
    """

    # Data Model (DB) Fields
    course = models.ForeignKey(Course)
    instructor = models.ForeignKey(User, verbose_name='User(s) Instructing Course')

    def __unicode__(self):
        return (self.course.name + " - " + self.instructor.username)

    def validate_unique(self, exclude=None):
        """ Verifies Instructor is unique (raises ValidationError when not). """
        if self.course and self.instructor:
            instructors = Instructor.objects.all().filter(course=self.course).filter(instructor=self.instructor)
            for instructor in instructors: # When Instructor exists, verify same object as being edited:
                if instructor.pk != self.pk:
                    error_msg = 'Existing Instructor binding ' + self.course.name + '/' + self.instructor.username + '!'
                    raise ValidationError({NON_FIELD_ERRORS: [error_msg]})
        super(Instructor, self).validate_unique()

    def delete(self):
        """ Remove User from Instructor Group on Delete (if User is no longer Instructor in Classcomm). """
        try:
            if Instructor.objects.all().filter(instructor=self.instructor).count() <= 1:
                instructor_group = Group.objects.get(name="Instructor")
                self.instructor.groups.remove(instructor_group)
        except ObjectDoesNotExist:
            pass
        super(Instructor, self).delete()

    def save(self):
        """ Add User to admin and Instructor Group on save (if not already). """
        if not self.instructor.is_staff:
            self.instructor.is_staff = True
            self.instructor.save()
        try:
            if self.instructor.groups.all().filter(name="Instructor").count() == 0:
                instructor_group = Group.objects.get(name="Instructor")
                self.instructor.groups.add(instructor_group)
        except ObjectDoesNotExist:
            pass
        super(Instructor, self).save()
# EndClass

class Mentor(models.Model):
    """ Data Model binding a Mentor to Course object.  This is the preferred way
        for instantiating a mentor, but there also exists an optional Enrollment level mentor binding
        in the Enrollment object for limiting mentors to a specific student's Enrollment.
    """

    # Data Model (DB) Fields
    course = models.ForeignKey(Course)
    mentor = models.ForeignKey(User, verbose_name='User(s) Mentoring entire Course')

    def __unicode__(self):
        return (self.course.name + " - " + self.mentor.username)

    def validate_unique(self, exclude=None):
        """ Verifies Mentor is unique (raises ValidationError when not). """
        if self.course and self.mentor:
            mentors = Mentor.objects.all().filter(course=self.course).filter(mentor=self.mentor)
            for mentor in mentors: # When Mentor exists, verify same object as being edited:
                if mentor.pk != self.pk:
                    error_msg = 'Existing Mentor binding ' + self.course.name + '-' + self.mentor.username + '!'
                    raise ValidationError({NON_FIELD_ERRORS: [error_msg]})
        super(Mentor, self).validate_unique()

    def delete(self):
        """ Remove User from Mentor Group on Delete (if User is no longer Mentor in Classcomm). """
        try:
            if Mentor.objects.all().filter(mentor=self.mentor).count() <= 1:
                mentor_group = Group.objects.get(name="Mentor")
                self.mentor.groups.remove(mentor_group)
        except ObjectDoesNotExist:
            pass
        super(Mentor, self).delete()

    def save(self):
        """ Add User to admin and Mentor Group on save (if not already). """
        if not self.mentor.is_staff:
            self.mentor.is_staff = True
            self.mentor.save()
        try:
            if self.mentor.groups.all().filter(name="Mentor").count() == 0:
                mentor_group = Group.objects.get(name="Mentor")
                self.mentor.groups.add(mentor_group)
        except ObjectDoesNotExist:
            pass
        super(Mentor, self).save()
# EndClass

# Static Model Define for Enrollment Access Condition flags.
ENROLLMENT_ACCESS = (
    ('Normal', 'Normal'),
    ('Active', 'Active'),
    ('Disabled', 'Disabled'),
)
class Enrollment(models.Model):
    """
        Data Model representing any student's (User) Enrollment in a Course.
        Enrollments must specify the student, course, start_date and access_mode (default 'Normal').
        Enrollments may optionally specify a mentor and length_override.
    """
    
    # Data Model (DB) Fields
    student = models.ForeignKey(User, verbose_name='The Enrolled', related_name='enrollment_student',
                                help_text="Enroll this user as student in Course.")
    course = models.ForeignKey(Course, verbose_name='In Course', help_text="Course of Enrollment.")
    start_date = models.DateField('Start Date', help_text="Date Enrollment begins.")
    access_mode = models.CharField('Access Mode', max_length=15, choices=ENROLLMENT_ACCESS, default='Normal',
        help_text="Normal: User granted access at start_date for course.length or length_override if specified." +
        "<br />Active: User granted access indefinitely, or until this flag is changed." +
        "<br />Disabled: User denied access indefinitely, or until this flag is changed.")
    mentor = models.ForeignKey(User, verbose_name='Individual Mentor', related_name='enrollment_mentor',
        null=True, blank=True,
        help_text="Optional Student-level mentorship?  Mentors typically defined at Course level with Mentor object.")
    length_override = models.IntegerField('Enrollment Length Override',
        help_text="Override Course.length (duration in weeks) for this Enrollment?",
        null=True, blank=True)

    def __unicode__(self):
        return (self.student.username +  " - " + self.course.name)

    def validate_unique(self, exclude=None):
        """ Verifies Enrollment uniqueness (may raise ValidationError).
            The Exceptions generated here are caught and rendered by Django admin and ModelForms. """
        if self.student and self.course:
            enrollments = Enrollment.objects.all().filter(student=self.student).filter(course=self.course)
            for enrollment in enrollments: # When Enrollment exists, verify same object as being edited:
                if enrollment.pk != self.pk:
                    error_msg = 'Existing Enrollment for ' + self.student.username + '/' + self.course.name + '!'
                    raise ValidationError({NON_FIELD_ERRORS: [error_msg]})
        super(Enrollment, self).validate_unique()

    def delete(self):
        """ Remove User from Mentor Group on Delete (if User is no longer Mentor in Classcomm). """
        try:
            if Mentor.objects.all().filter(mentor=self.mentor).count() <= 1:
                mentor_group = Group.objects.get(name="Mentor")
                self.mentor.groups.remove(mentor_group)
        except ObjectDoesNotExist:
            pass
        super(Enrollment, self).delete()

    def save(self):
        """ Add User to admin and Mentor Group on save (if not already). """
        if self.mentor:
            if not self.mentor.is_staff:
                self.mentor.is_staff = True
                self.mentor.save()
            try:
                if self.mentor.groups.all().filter(name="Mentor").count() == 0:
                    mentor_group = Group.objects.get(name="Mentor")
                    self.mentor.groups.add(mentor_group)
            except ObjectDoesNotExist:
                pass
        super(Enrollment, self).save()
# EndClass

class Assignment(models.Model):
    """ Data Model representing a Course Assignment. """
    
    def get_assignment_path(self, filename):
        """ Passed as callable to ProtectedFileField upload_to parameter. """
        return os.path.join('uploads/provided_files/', 
            self.course.department.name, 
            self.course.name, 
            filename)

    # Data Model (DB) Fields
    course = models.ForeignKey(Course)
    name = models.CharField('Title', max_length=200, help_text='Assignments are ordered alphabetically by name, ' +
                                                 'so organize them like: AS.01, AS.02, AS.03, etc.')
    details = models.TextField('Details')
    points_possible = models.IntegerField('Point Value', default=20,
       help_text="Enter 0 to make assignment of no consequence.")
    display_points_possible = models.BooleanField("Allow students to view points possible?", default=True)
    provided_files = ProtectedFileField(upload_to=get_assignment_path, max_length=250, null=True, blank=True,
       help_text='Optionally supply a file with this assignment.')
    apply_due_date = models.BooleanField("Apply a default Assignment Due Date?")
    weeks_after = models.IntegerField('Due Weeks After Enrollment', default=0,
       help_text="DueDate is a calculated offset of weeks_after + days_after from the Enrollment start_date.")
    days_after = models.IntegerField('Due Days After Enrollment', default=0,
       help_text="DueDate is a calculated offset of weeks_after + days_after from the Enrollment start_date.")
    allow_late = models.BooleanField("Allow late homework Submissions?", default=True)
    disable_submissions = models.BooleanField("Disable online Submissions for this Assignment?", default=False)

    def __unicode__(self):
        return (self.course.name + " - " + self.name)

    def validate_unique(self, exclude=None):
        """ Verifies Assignment is unique (may raise ValidationError when not).
            The Exceptions generated here are caught and rendered by Django admin and ModelForms. """
        if "course" and "name" not in exclude:
            assignments = Assignment.objects.all().filter(course=self.course).filter(name=self.name)
            for assignment in assignments:
                if assignment.pk != self.pk:
                    error_msg = 'Already existing Assignment with same Name in ' + self.course.name +'!'
                    raise ValidationError({NON_FIELD_ERRORS: [error_msg]})
        super(Assignment, self).validate_unique()
# EndClass

class DueDateOverride(models.Model):
    """ Data representing a Due Date Override for a specific Enrollment's Assignment. """

    # Data Model (DB) Fields
    enrollment = models.ForeignKey(Enrollment, verbose_name='Enrollment',
       help_text="Specify Enrollment for which to apply this Due Date.")
    assignment = models.ForeignKey(Assignment,
       help_text="Specify Assignment for which to override the default Due Date.")
    weeks_after = models.IntegerField('Weeks after start_date', default=0,
       help_text="Due Date is a calculated offset of weeks_after + days_after from the Enrollment.start_date.")
    days_after = models.IntegerField('Days after start_date', default=0,
       help_text="Due Date is a calculated offset of weeks_after + days_after from the Enrollment.start_date.")
    allow_late = models.BooleanField("Allow late homework Submissions?", default=True)

    def __unicode__(self):
        return (self.enrollment.__unicode__() + " - " + self.assignment.name)

    def validate_unique(self, exclude=None):
        """ Verifies DueDateOverride properties (may raise ValidationError).
            The Exceptions generated here are caught and rendered by Django admin and ModelForms. """
        if self.assignment and self.enrollment and self.enrollment.course:  # Verify Assignment corresponds Enrollment
            if self.assignment.course != self.enrollment.course:
                error_msg = 'Selected Assignment is not valid within Enrollment.course!'
                raise ValidationError({NON_FIELD_ERRORS: [error_msg]})
            DDOs = DueDateOverride.objects.all().filter(enrollment=self.enrollment).filter(assignment=self.assignment)
            for DDO in DDOs: # When similar DDOs exists, Verify same object as being edited:
                if DDO.pk != self.pk:
                    error_msg = 'Existing DDO for this Enrollment/Assignment combo!'
                    raise ValidationError({NON_FIELD_ERRORS: [error_msg]})
        super(DueDateOverride, self).validate_unique()
# EndClass

class Submission(models.Model):
    """ Data Model representing a student's homework Submission. """
    
    def get_grade_path(self, filename):
        """ Passed as a callable to ProtectedFileField upload_to parameter. """
        savename = str(self.assignment.name) + '__' + os.path.splitext(filename)[1]
        return os.path.join('uploads/submitted_files/', 
            self.enrollment.course.department.name, 
            self.enrollment.course.name,
            self.enrollment.student.username,
            savename)

    # Data Model (DB) Fields
    date = models.DateTimeField(editable=False, auto_now_add=True)
    enrollment = models.ForeignKey(Enrollment, verbose_name='Enrollment')
    assignment = models.ForeignKey(Assignment)
    file = ProtectedFileField(upload_to=get_grade_path, max_length=250)
    on_time = models.BooleanField("Submitted on time?", default=True)
    add_checkscript = models.BooleanField("Add to checkscript?", default=True)

    def __unicode__(self):
        return (self.enrollment.__unicode__() + " - " + self.assignment.name)

    def  validate_unique(self, exclude=None):
        """ Verifies Submission properties; set initial params (may raise ValidationError).
            The Exceptions generated here are caught and rendered by Django admin and ModelForms. """
        if self.assignment and self.enrollment and self.enrollment.course:  # Verify Assignment corresponds Enrollment
            if self.assignment.course != self.enrollment.course:
                error_msg = 'Selected Assignment is not valid within Enrollment.course!'
                raise ValidationError({NON_FIELD_ERRORS: [error_msg]})
            submissions = Submission.objects.all().filter(enrollment=self.enrollment).filter(assignment=self.assignment)
            for submission in submissions: # Verify any similar Submissions are the same object as being edited:
                if submission.pk != self.pk:
                    error_msg = 'Existing Submission for this Enrollment/Assignment combo!'
                    raise ValidationError({NON_FIELD_ERRORS: [error_msg]})
        super(Submission, self).validate_unique()

    def save(self):
        """ Set add_checkscript flag when the object is first created. """
        if not self.id: # Set add_checkscript flag when object is first created:
            self.add_checkscript = True
        super(Submission, self).save()
# EndClass

class Grade(models.Model):
    """ This class represents an Assignment Grade for a specific Enrollment. """
    
    def get_grade_path(self, filename):
        """ Passed as callable to ProtectedFileField upload_to parameter. """
        savename = str(self.assignment.name) + '__' + os.path.splitext(filename)[1]
        return os.path.join('uploads/returned_files/', 
            self.enrollment.course.department.name, 
            self.enrollment.course.name,
            self.enrollment.student.username,
            savename)

    # Data Model (DB) Fields
    return_date = models.DateTimeField(auto_now_add=True)
    enrollment = models.ForeignKey(Enrollment, verbose_name='Student Enrollment', related_name='grade_enrollment')
    assignment = models.ForeignKey(Assignment, verbose_name='Grading Assignment', related_name='grade_assignment')
    points_earned = models.DecimalField('Points Earned', max_digits=5, decimal_places=2)
    returned_files = ProtectedFileField(upload_to=get_grade_path, max_length=250, null=True, blank=True)
    comments = models.TextField('Comments', null=True, blank=True,
        help_text="Form accepts XHTML but use it mindfully--The view should not be altered!")

    def __unicode__(self):
        return (self.enrollment.__unicode__() + " - " + self.assignment.name)

    def validate_unique(self, exclude=None):
        """ Verifies Grade uniqueness properties (raises ValidationError otherwise).
            Exceptions generated are caught and rendered by Django ModelForm.is_valid and model.full_clean. """
        if self.assignment and self.enrollment and self.enrollment.course:  # Verify Assignment corresponds Enrollment
            if self.assignment.course != self.enrollment.course:
                error_msg = 'Selected Assignment is not valid within Enrollment.course!'
                raise ValidationError({NON_FIELD_ERRORS: [error_msg]})
            # Verify any similar Grade is the same as object being edited:
            grades = Grade.objects.all().filter(enrollment=self.enrollment).filter(assignment=self.assignment)
            for grade in grades:
                if grade.pk != self.pk:
                    error_msg = 'Existing Grade for this Enrollment/Assignment combo!'
                    raise ValidationError({NON_FIELD_ERRORS: [error_msg]})
        super(Grade, self).validate_unique()

    def save(self):
        """ Saves and updates corresponding Submission.add_checkscript flag. """
        super(Grade, self).save()
        submissions = Submission.objects.all().filter(enrollment=self.enrollment).filter(assignment=self.assignment)
        for submission in submissions:
            submission.add_checkscript = False
            submission.save()

    def delete(self):
        """ Deletes Grade and update any corresponding Submission.add_checkscript flag. """
        submissions = Submission.objects.all().filter(enrollment=self.enrollment).filter(assignment=self.assignment)
        for submission in submissions:
            submission.add_checkscript = True
            submission.save()
        super(Grade, self).delete()
# EndClass

class ExtraCredit(models.Model):
    """ This class represents a unit of Extra Credit for a specific Enrollment. """

    # Data Model (DB) Fields
    return_date = models.DateTimeField(auto_now_add=True)
    name = models.CharField('Name Extra Credit', max_length=100)
    enrollment = models.ForeignKey(Enrollment,
        verbose_name='Student Enrollment', related_name='ec_enrollment')
    points_earned = models.DecimalField('Points Earned', max_digits=5, decimal_places=2)
    comments = models.TextField('Comments', null=True, blank=True,
        help_text="Optionally return comments with these extra points.")

    def __unicode__(self):
        return (self.enrollment.__unicode__() + " - " + self.name)

    def validate_unique(self, exclude=None):
        """ Verify that this extra credit has a unique name for the enrollment. (May raise ValidationError)
            Exceptions generated are caught and rendered by Django ModelForm.is_valid and model.full_clean. """
        extra_credits = ExtraCredit.objects.all().filter(enrollment=self.enrollment).filter(name=self.name)
        for ec in extra_credits:
            if ec.pk != self.pk:
                error_msg = 'Existing Extra Credit for this Enrollment with currently specified name!'
                raise ValidationError({NON_FIELD_ERRORS: [error_msg]})
        super(ExtraCredit, self).validate_unique()
# EndClass

class Information(models.Model):
    """ Data Model representing what is a Course Information. """

    # Data Model (DB) Fields
    department = models.ForeignKey(Department, verbose_name='Tag Department',
       related_name='info_department', null=True, blank=True,
       help_text="Use this field to tag this info to a specific Department.")
    course = models.ForeignKey(Course, verbose_name='Tag Course',
       related_name='info_course', null=True, blank=True,
       help_text="Use this field to tag this info to a specific Course.")
    name = models.CharField('Information Title', max_length=100)
    description = models.CharField('Short Description', max_length=200)
    details = models.TextField('Information Markup',
       help_text="Form accepts HTML, but use it mindfully--View display should not be altered!")

    def __unicode__(self):
        return self.name
# EndClass

class Resource(models.Model):
    """ Data Model representing what is a Course Resource. """
    
    # Data Model (DB) Fields
    department = models.ForeignKey(Department, verbose_name='Tag Department',
        related_name='resource_department', null=True, blank=True,
        help_text="Use this field to tag this resource to a specific department.")
    course = models.ForeignKey(Course, verbose_name='Tag Course',
        related_name='resource_course', null=True, blank=True,
        help_text="Use this field to tag this resource to a specific course.")
    name = models.CharField('Resource Name', max_length=100)
    url = models.CharField('Main Resource URL', max_length=200, null=True, 
        blank=True, help_text="Optional URL to external resource.")
    details = models.TextField('Resource Details',
        help_text="Form accepts HTML, but use it mindfully--View display should not be altered!")

    def __unicode__(self):
        return self.name
# EndClass

class Announcement(models.Model):
    """ Represents an Announcement in the classcomm system. """

    # Data Model (DB) Fields
    pub_date = models.DateTimeField(blank=True)
    author = models.ForeignKey(User, verbose_name='Author', null=True, blank=True,
                               help_text='When blank, this field will auto-fill to be the current User on save.')
    make_global = models.BooleanField('Make Global Announcement?', help_text='Only super users may set this flag!')
    department = models.ForeignKey(Department, verbose_name='Tag Department',
        related_name='announcement_department', null=True, blank=True,
        help_text="Use this field to tag this announcement to a specific department.")
    course = models.ForeignKey(Course, verbose_name='Tag Course',
        related_name='announcement_course', null=True, blank=True,
        help_text="Use this field to tag this announcement to a specific course.")
    headline = models.CharField(max_length=100)
    content = models.TextField('Announcement Markup',
        help_text="Form accepts HTML, but use it mindfully--View display should not be altered!")

    def __unicode__(self):
        return self.headline

    def clean_fields(self, exclude=['author',]):
        """ Implement wrapper for clean_fields to exclude author so we can fill in on save. """
        super(Announcement, self).clean_fields(exclude)
    # EndDef

    def clean(self):
        """ Implement auto fill pub_date. """
        if not self.pub_date:
            self.pub_date = datetime.today()
        super(Announcement, self).clean()
    # EndDef

    def save(self):
        """ Implement auto fill pub_date; Raises ValidationError when missing Author. """
        if not self.author:
            raise ValidationError('New Announcements require an Author be specified!')
        if not self.pub_date:
            self.pub_date = datetime.today()
        super(Announcement, self).save()
    # EndDef
# EndClass

