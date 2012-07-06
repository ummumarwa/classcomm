from django.db.models.signals import pre_save
from django.dispatch import receiver
from django.contrib.auth.models import Group, User
from django.core.exceptions import ObjectDoesNotExist
from classcomm.student_portal.models import Enrollment, Instructor, Mentor, Course

import logging
logger = logging.getLogger('student_portal')

@receiver(pre_save, sender=Course)
def recover_director_perms(sender, **kwargs):
    """ Signal receiver to detect Mentor changes and possibly revoke permissions. """
    instance = kwargs['instance']
    try:
        course = Course.objects.get(id__exact=instance.id)
        if course.director != instance.director: # Detect when Director User changes and try reverting permissions
            courses = Course.objects.all().filter(director=course.director)
            if (courses.count() <= 1): # When last remaining Director role, remove from Director Group.
                director_group = Group.objects.get(name="Director")
                course.director.groups.remove(director_group)
    except ObjectDoesNotExist: # New Course obj, or Default Groups don't exist
        return
# EndDef

@receiver(pre_save, sender=Instructor)
def recover_instructor_perms(sender, **kwargs):
    """ Signal receiver to detect Instructor changes and possibly revoke permissions. """
    instance = kwargs['instance']
    try:
        instructor = Instructor.objects.get(id__exact=instance.id)
        if instructor.instructor != instance.instructor: # Detect when Instructor User changes
            instructors = Instructor.objects.all().filter(instructor=instructor.instructor)
            if (instructors.count() <= 1): # When last remaining Instructor role, remove from Instructor Group.
                instructor_group = Group.objects.get(name="Instructor")
                instructor.instructor.groups.remove(instructor_group)
    except ObjectDoesNotExist: # New Instructor obj, or Default Groups don't exist
        return
# EndDef

@receiver(pre_save, sender=Mentor)
def recover_mentor_perms(sender, **kwargs):
    """ Signal receiver to detect Mentor changes and possibly revoke permissions. """
    instance = kwargs['instance']
    try:
        mentor = Mentor.objects.get(id__exact=instance.id)
        if mentor.mentor != instance.mentor: # Detect when Mentor User has changed
            mentors = Mentor.objects.all().filter(mentor=mentor.mentor)
            if (mentors.count() <= 1): # When last remaining Mentor role, remove from Mentor Group.
                mentor_group = Group.objects.get(name="Mentor")
                mentor.mentor.groups.remove(mentor_group)
    except ObjectDoesNotExist: # New Mentor obj, or Default Groups don't exist
        return
# EndDef

@receiver(pre_save, sender=Enrollment)
def recover_mentor_assign_perms(sender, **kwargs):
    """ Signal receiver to detect Mentor changes and possibly revoke permissions. """
    instance = kwargs['instance']
    try:
        enrollment = Enrollment.objects.get(id__exact=instance.id)
        if enrollment.mentor != instance.mentor: # Detect when Enrollment.Mentor User has changed
            mentors = Mentor.objects.all().filter(mentor=enrollment.mentor)
            if (mentors.count() <= 1): # When last remaining Mentor role, remove from Mentor Group.
                mentor_group = Group.objects.get(name="Mentor")
                enrollment.mentor.groups.remove(mentor_group)
    except ObjectDoesNotExist: # New Enrollment obj, or Default Groups don't exist
        return
# EndDef
