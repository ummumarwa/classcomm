from classcomm.student_portal.models import *
from django.contrib import admin
from django.db.models import Q

class CourseInline(admin.TabularInline):
    """ Course Inline Customization for Departments. """
    model = Course
    extra = 1

    def queryset(self, request):
        """ This queryset needs related information for optimized processing. """
        return super(CourseInline, self).queryset(request).select_related('director')
# EndClass

class DepartmentAdmin(admin.ModelAdmin):
    """ Admin customizations for Department Models. """
    list_display = ['name']
    search_fields = ['name']
    inlines = [CourseInline]
# EndClass

class InstructorInline(admin.TabularInline):
    """ Instructor Inline Customization for Courses. """
    model = Instructor
    extra = 1

    def queryset(self, request):
        """ This queryset needs related information for optimized processing. """
        return super(InstructorInline, self).queryset(request).select_related('instructor')
# EndClass

class MentorInline(admin.TabularInline):
    """ Mentor Inline Customization for Courses. """
    model = Mentor
    extra = 1

    def queryset(self, request):
        """ This queryset needs related information for optimized processing. """
        return super(MentorInline, self).queryset(request).select_related('mentor')
# EndClass

class AssignmentInline(admin.TabularInline):
    """ Assignment Inline Customization for Courses. """
    model = Assignment
    extra = 1
# EndClass

class CourseAdmin(admin.ModelAdmin):
    """ Admin customization for Course Models. """
    list_display = ['name', 'department', 'director', 'open_enrollments']
    list_filter = ['department', 'open_enrollments', 'enrollment_length']
    list_select_related = True
    search_fields = ['name', 'description', 'department__name', 'director__username', 'director__email']
    fieldsets = (
        (None, {
            'fields': ('department', 'name', 'enrollment_length', 'description')
        }),
        ('Advanced options', {
            'classes': ('collapse',),
            'fields': ('director', 'open_enrollments')
        }),
    )
    inlines = [InstructorInline, MentorInline, AssignmentInline]

    def queryset(self, request):
        """ Taylor queryset for request.user's active Classcomm roles. """
        if request.user.is_superuser:
            return super(CourseAdmin, self).queryset(request).select_related('department', 'director')
        else:
            return Course.objects.all().filter(Q(director=request.user) |
                            Q(instructor__instructor=request.user)).distinct().select_related('department', 'director')
# EndClass

class InstructorAdmin(admin.ModelAdmin):
    """ Admin customization for Instructor Models. """
    actions = ['delete_selected_full']
    list_display = ['course', 'instructor']
    list_filter = ['course', 'instructor']
    list_select_related = True
    search_fields = ['course', 'instructor']

    def get_actions(self, request):
        """ Override get_actions function to list only our delete_selected_full for use. """
        actions = super(InstructorAdmin, self).get_actions(request)
        del actions['delete_selected']
        return actions

    def delete_selected_full(self, request, queryset):
        """ For each selected object we want to explicitly call Instructor model delete. """
        for obj in queryset:
            obj.delete()
        if queryset.count() == 1:
            message_bit = "1 instructor entry was"
        else:
            message_bit = "%s instructor entries were" % queryset.count()
        self.message_user(request, "%s successfully deleted." % message_bit)
    delete_selected_full.short_description = "Delete selected instructor entries"

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        """ Filter ForeignKeys (with related data) based on Assigned Active User roles (on Add/Edit forms). """
        if db_field.name == "course":
            if request.user.is_superuser:
                kwargs["queryset"] = Course.objects.all().select_related('department')
            else:
                kwargs["queryset"] = Course.objects.all().filter(Q(director=request.user) |
                                      Q(instructor__instructor=request.user)).distinct().select_related('department')
        else:
            kwargs["queryset"] =  formfield_for_foreignkey_generic(db_field, request)
        return super(InstructorAdmin, self).formfield_for_foreignkey(db_field, request, **kwargs)

    def queryset(self, request):
        """ Taylor queryset for request.user's active Classcomm roles. """
        if request.user.is_superuser:
            return super(InstructorAdmin, self).queryset(request).select_related()
        else:
            return Instructor.objects.all().filter(Q(course__director=request.user) |
                            Q(instructor=request.user)).distinct().select_related()
# EndClass

class MentorAdmin(admin.ModelAdmin):
    """ Admin customization for Mentor Models.

    """
    actions = ['delete_selected_full']
    list_display = ['course', 'mentor']
    list_filter = ['course', 'mentor']
    list_select_related = True
    search_fields = ['course', 'mentor']

    def get_actions(self, request):
        """ Override get_actions function to list only our delete_selected_full for use. """
        actions = super(MentorAdmin, self).get_actions(request)
        del actions['delete_selected']
        return actions

    def delete_selected_full(self, request, queryset):
        """ For each selected object we want to explicitly call Mentor model delete. """
        for obj in queryset:
            obj.delete()
        if queryset.count() == 1:
            message_bit = "1 mentor entry was"
        else:
            message_bit = "%s mentor entries were" % queryset.count()
        self.message_user(request, "%s successfully deleted." % message_bit)
    delete_selected_full.short_description = "Delete selected mentor entries"

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        """ Filter ForeignKeys (with related data) based on Assigned Active User roles (on Add/Edit forms). """
        if db_field.name == "course":
            if request.user.is_superuser:
                kwargs["queryset"] = Course.objects.all().select_related('department')
            else:
                kwargs["queryset"] = Course.objects.all().filter(Q(director=request.user) |
                                      Q(instructor__instructor=request.user)).distinct().select_related('department')
        else:
            kwargs["queryset"] =  formfield_for_foreignkey_generic(db_field, request)
        return super(MentorAdmin, self).formfield_for_foreignkey(db_field, request, **kwargs)

    def queryset(self, request):
        """ Taylor queryset for request.user's active Classcomm roles. """
        if request.user.is_superuser:
            return super(MentorAdmin, self).queryset(request).select_related()
        else:
            return Mentor.objects.all().filter(Q(course__director=request.user) |
                            Q(course__instructor__instructor=request.user) |
                            Q(mentor=request.user)).distinct().select_related()
# EndClass

class EnrollmentAdmin(admin.ModelAdmin):
    """ Admin customization for Enrollment Models.

    """
    date_hierarchy = 'start_date'
    list_display = ['start_date', 'student', 'course', 'mentor', 'access_mode']
    list_filter = ['course', 'access_mode', 'mentor']
    list_select_related = True
    search_fields = ['student__username', 'student__email', 'course__name', 'mentor__username']
    fieldsets = (
        (None, {
            'fields': ('student', 'course', 'start_date')
        }),
        ('Advanced options', {
            'classes': ('collapse',),
            'fields': ('access_mode', 'mentor', 'length_override')
        }),
    )

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        """ Filter ForeignKeys (with related data) based on Assigned Active User roles (on Add/Edit forms).
            We do not use the generic here because we want to be more restrictive about What Courses.
        """
        if db_field.name == "course":
            if request.user.is_superuser:
                kwargs["queryset"] = Course.objects.all().select_related('department')
            else:
                kwargs["queryset"] = Course.objects.all().filter(Q(director=request.user) |
                                      Q(instructor__instructor=request.user)).distinct().select_related('department')
        return super(EnrollmentAdmin, self).formfield_for_foreignkey(db_field, request, **kwargs)

    def queryset(self, request):
        """ For Superusers: Get all Assignments (w/ related_data) as typical by parent method.
            Staff Users: Get all Assignments for Courses where request.user is director or instructor. """
        if request.user.is_superuser:
            return super(EnrollmentAdmin, self).queryset(request).select_related('student', 'course', 'mentor')
        else:
            return Enrollment.objects.all().filter(Q(course__director=request.user) |
                        Q(course__instructor__instructor=request.user)).distinct().select_related('student',
                                                                                                  'course', 'mentor')
# EndClass

class AssignmentAdmin(admin.ModelAdmin):
    """ Admin customizations for Assignment Models.

    """
    list_display = ['name', 'course', 'display_points_possible', 'points_possible', 'apply_due_date']
    list_filter = ['course', 'apply_due_date', 'disable_submissions']
    search_fields = ['name', 'course__name', 'course__department__name']
    fieldsets = (
        (None, {
            'fields': ('course', 'name', 'details', 'points_possible', 'provided_files')
        }),
        ('Advanced options', {
            'classes': ('collapse',),
            'fields': ('apply_due_date', 'weeks_after', 'days_after', 'allow_late',
                       'display_points_possible', 'disable_submissions')
        }),
    )

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        """ Filter ForeignKeys (with related data) based on Assigned Active User roles (on Add/Edit forms). """
        if db_field.name == "course":
            if request.user.is_superuser:
                kwargs["queryset"] = Course.objects.all().select_related('department')
            else:
                kwargs["queryset"] = Course.objects.all().filter(Q(director=request.user) |
                                      Q(instructor__instructor=request.user)).distinct().select_related('department')
        return super(AssignmentAdmin, self).formfield_for_foreignkey(db_field, request, **kwargs)

    def queryset(self, request):
        """ This QuerySet gets related information for optimized processing.
            For Superusers: Get all Assignments (w/ related_data) as typical by parent method.
            Staff Users: Get all Assignments for Courses request.user is director or instructor. """
        if request.user.is_superuser:
            return super(AssignmentAdmin, self).queryset(request).select_related('course', 'course__department')
        else:
            return Assignment.objects.all().filter(Q(course__director=request.user) |
                        Q(course__instructor__instructor=request.user)).distinct().select_related('course',
                                                                                                  'course__department')
# EndClass

class DueDateOverrideAdmin(admin.ModelAdmin):
    """ Admin customizations for DueDateOverride Models.

    """
    list_display = ['enrollment', 'assignment', 'weeks_after', 'days_after', 'allow_late']
    list_select_related = True
    search_fields = ['enrollment__course__name', 'enrollment__student__username',
                     'enrollment__student__email', 'assignment__name']

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        """ Filter ForeignKeys (with related data) based on Assigned Active User roles (on Add/Edit forms). """
        kwargs["queryset"] = formfield_for_foreignkey_generic(db_field, request)
        return super(DueDateOverrideAdmin, self).formfield_for_foreignkey(db_field, request, **kwargs)

    def queryset(self, request):
        """ This QuerySet gets related information for optimized processing.
            For Superusers: Get all DueDateOverrides (w/ related_data) as typical by parent method.
            Staff Users: Get all Assignments for Courses request.user is director or instructor. """
        if request.user.is_superuser:
            return super(DueDateOverrideAdmin, self).queryset(request).select_related('course')
        else:
            return DueDateOverride.objects.all().filter(Q(enrollment__course__director=request.user) |
                        Q(enrollment__course__instructor__instructor=request.user) |
                        Q(enrollment__course__mentor__mentor=request.user) |
                        Q(enrollment__mentor=request.user)).distinct().select_related('course')
# EndClass

class GradeInline(admin.TabularInline):
    """ Grade Inline Customizations for Grades.

    """
    model = Grade
    extra = 1
    max_num = 1
# EndClass

class SubmissionAdmin(admin.ModelAdmin):
    """ Admin customizations for Submission Models.

    """
    date_hierarchy = 'date'
    list_display = ['date', 'enrollment', 'assignment', 'on_time', 'add_checkscript']
    readonly_fields = ['date']
    search_fields = ['enrollment__course__name', 'enrollment__course__department__name',
                     'enrollment__student__username', 'enrollment__student__email', 'assignment__name']
    fieldsets = (
        (None, {
            'fields': ('date', 'enrollment', 'assignment', 'file')
        }),
        ('Advanced options', {
            'classes': ('collapse',),
            'fields': ('on_time', 'add_checkscript')
        }),
    )

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        """ Filter ForeignKeys (with related data) based on Assigned Active User roles (on Add/Edit forms). """
        kwargs["queryset"] = formfield_for_foreignkey_generic(db_field, request)
        return super(SubmissionAdmin, self).formfield_for_foreignkey(db_field, request, **kwargs)

    def queryset(self, request):
        """ For Superusers: Get all Submissions (w/ related_data) as typical by parent method.
            Staff Users: Get all Submissions where request.user is director, instructor or mentor. """
        if request.user.is_superuser:
            return super(SubmissionAdmin, self).queryset(request).select_related()
        else:
            return Submission.objects.all().filter(Q(enrollment__course__director=request.user) |
                        Q(enrollment__course__instructor__instructor=request.user) |
                        Q(enrollment__course__mentor__mentor=request.user) |
                        Q(enrollment__mentor=request.user)).distinct().select_related()
# EndClass

class GradeAdmin(admin.ModelAdmin):
    """ Admin customizations for Grade Models.

    """
    date_hierarchy = 'return_date'
    list_display = ['return_date', 'enrollment', 'assignment', 'points_earned']
    list_select_related = True
    search_fields = ['enrollment__course__name', 'enrollment__course__department__name',
                     'enrollment__student__username', 'enrollment__student__email', 'assignment__name', 'comments']

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        """ Filter ForeignKeys (with related data) based on Assigned Active User roles (on Add/Edit forms). """
        kwargs["queryset"] = formfield_for_foreignkey_generic(db_field, request)
        return super(GradeAdmin, self).formfield_for_foreignkey(db_field, request, **kwargs)

    def queryset(self, request):
        """ For Superusers: Get all Grades (w/ related_data) as typical by parent method.
            Staff Users: Get all Grades where request.user is director, instructor or mentor. """
        if request.user.is_superuser:
            return super(GradeAdmin, self).queryset(request).select_related()
        else:
            return Grade.objects.all().filter(Q(enrollment__course__director=request.user) |
                        Q(enrollment__course__instructor__instructor=request.user) |
                        Q(enrollment__course__mentor__mentor=request.user) |
                        Q(enrollment__mentor=request.user)).distinct().select_related()
# EndClass

class ExtraCreditAdmin(admin.ModelAdmin):
    """ Admin customizations for Grade Models.

    """
    date_hierarchy = 'return_date'
    list_display = ['return_date', 'enrollment']
    list_select_related = True
    search_fields = ['enrollment__course__name', 'enrollment__student__username', 'enrollment__student__email',
                     'assignment__name', 'comments']

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        """ Filter ForeignKeys (with related data) based on Assigned Active User roles (on Add/Edit forms). """
        kwargs["queryset"] = formfield_for_foreignkey_generic(db_field, request)
        return super(ExtraCreditAdmin, self).formfield_for_foreignkey(db_field, request, **kwargs)

    def queryset(self, request):
        """ For Superusers: Get all Grades (w/ related_data) as typical by parent method.
            Staff Users: Get all Grades where request.user is director, instructor or mentor. """
        if request.user.is_superuser:
            return super(ExtraCreditAdmin, self).queryset(request).select_related()
        else:
            return ExtraCredit.objects.all().filter(Q(enrollment__course__director=request.user) |
                        Q(enrollment__course__instructor__instructor=request.user) |
                        Q(enrollment__course__mentor__mentor=request.user) |
                        Q(enrollment__mentor=request.user)).distinct().select_related()
# EndClass

class InformationAdmin(admin.ModelAdmin):
    """ Admin customization for Information Models.

    """
    list_display = ['department', 'course', 'name']
    list_filter = ['department', 'course']
    search_fields = ['name', 'department__name', 'course__name', 'description']

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        """ Filter ForeignKeys (with related data) based on Assigned Active User roles (on Add/Edit forms). """
        kwargs["queryset"] = formfield_for_foreignkey_generic(db_field, request)
        return super(InformationAdmin, self).formfield_for_foreignkey(db_field, request, **kwargs)

    def queryset(self, request):
        """ For Superusers: Get all Information (w/ related_data) as typical by parent method.
            Staff Users: Get all Information for Courses request.user is director, instructor or mentor. """
        if request.user.is_superuser:
            return super(InformationAdmin, self).queryset(request).select_related('course', 'department')
        else:
            return Information.objects.all().filter(Q(course__director=request.user) |
                        Q(course__instructor__instructor=request.user) |
                        Q(course__mentor__mentor=request.user)).distinct().select_related('course', 'department')
# EndClass

class ResourceAdmin(admin.ModelAdmin):
    """ Admin customization for Resource Models.

    """
    list_display = ['department', 'course', 'name']
    list_filter = ['department', 'course']
    search_fields = ['name', 'department__name', 'course__name', 'url']

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        """ Filter ForeignKeys (with related data) based on Assigned Active User roles (on Add/Edit forms). """
        kwargs["queryset"] =  formfield_for_foreignkey_generic(db_field, request)
        return super(ResourceAdmin, self).formfield_for_foreignkey(db_field, request, **kwargs)

    def queryset(self, request):
        """ For Superusers: Get all Resources (w/ related_data) as typical by parent method.
            Staff Users: Get all Resources for Courses request.user is director, instructor or mentor. """
        if request.user.is_superuser:
            return super(ResourceAdmin, self).queryset(request).select_related('course', 'department')
        else:
            return Resource.objects.all().filter(Q(course__director=request.user) |
                        Q(course__instructor__instructor=request.user) |
                        Q(course__mentor__mentor=request.user)).distinct().select_related('course', 'department')
# EndClass

class AnnouncementAdmin(admin.ModelAdmin):
    """ Admin customization for Announcement Models.

    """
    date_hierarchy = 'pub_date'
    list_filter = ['author', 'make_global', 'department', 'course']
    list_display = ['pub_date', 'author', 'headline', 'department', 'course', 'make_global']
    list_display_links = ['pub_date', 'headline']
    list_select_related = True
    search_fields = ['author__username', 'author__email', 'department__name', 'course__name', 'headline']
    fieldsets = (
        (None, {
            'fields': ('headline', 'department', 'course', 'content')
        }),
        ('Advanced options', {
            'classes': ('collapse',),
            'fields': ('author', 'pub_date', 'make_global')
        }),
    )

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        """ Filter ForeignKeys (with related data) based on Assigned Active User roles (on Add/Edit forms). """
        kwargs["queryset"] =  formfield_for_foreignkey_generic(db_field, request)
        return super(AnnouncementAdmin, self).formfield_for_foreignkey(db_field, request, **kwargs)

    def queryset(self, request):
        """ This query set gets related information for optimized processing. """
        if request.user.is_superuser:
            return super(AnnouncementAdmin, self).queryset(request).select_related('author', 'department', 'course')
        else:
            return Announcement.objects.all().filter(Q(course__director=request.user) |
                        Q(course__instructor__instructor=request.user) |
                        Q(course__mentor__mentor=request.user) |
                        Q(department__course__director=request.user) |
                        Q(department__course__instructor__instructor=request.user)).distinct().select_related('author',
                                                                                           'department', 'course')
    def save_model(self, request, obj, form, change):
        """ Auto-fill in author when blank on model saves.  Revert make_global flag for non super_user. """
        if not request.user.is_superuser:
            obj.make_global = False
            obj.save()
        if not obj.author:
            obj.author = request.user
            obj.save()
        return super(AnnouncementAdmin, self).save_model(request, obj, form, change)

    def save_formset(self, request, form, formset, change):
        """ Auto-fill in author when blank on formset saves. """
        instances = formset.save(commit=False)
        for instance in instances:
            if not request.user.is_superuser:
                instance.make_global = False
                instance.save()
            if not instance.author:
                instance.author = request.user
                instance.save()
        formset.save_m2m()
        return super(AnnouncementAdmin, self).save_formset(request, form, formset, change)
# EndClass

#############################
# Admin.py Helper Functions

def formfield_for_foreignkey_generic(db_field, request):
    """ Filter ForeignKeys (with related data) based on Assigned Active User roles (on Add/Edit forms).
        This function is generic because it contains the same logic needed across admin for filtering forms
        by active User permissions.

    """
    if db_field.name == "department":
        if request.user.is_superuser:
            return Department.objects.all()
        else:
            return Department.objects.all().filter(Q(course__director=request.user) |
                                      Q(course__instructor__instructor=request.user)).select_related('department')
    if db_field.name == "course":
        if request.user.is_superuser:
            return Course.objects.all().select_related('department')
        else:
            return Course.objects.all().filter(Q(director=request.user) |
                                      Q(instructor__instructor=request.user) |
                                      Q(mentor__mentor=request.user)).distinct().select_related('department')
    if db_field.name == "enrollment":
        if request.user.is_superuser:
            return Enrollment.objects.all().select_related('course', 'student')
        else:
            return Enrollment.objects.all().filter(Q(course__director=request.user) |
                        Q(course__instructor__instructor=request.user) |
                        Q(course__mentor__mentor=request.user) |
                        Q(mentor=request.user)).distinct().select_related('course', 'student')
    if db_field.name == "assignment":
        if request.user.is_superuser:
            return Assignment.objects.all().select_related('course')
        else:
            return Assignment.objects.all().filter(Q(course__director=request.user) |
                        Q(course__instructor__instructor=request.user) |
                        Q(course__mentor__mentor=request.user) |
                        Q(course__enrollment__mentor=request.user)).distinct().select_related('course')
    if db_field.name == "author":
        if request.user.is_superuser:
            return User.objects.all().filter(is_staff=True).select_related()
        else:  # Ideally we could set this to only be the existing author (if any) or the current user.
            return User.objects.all().filter(is_staff=True).select_related()
    if db_field.name == "instructor":
        if request.user.is_superuser:
            return User.objects.all().select_related()
        else:  # Currently we are filtering the Users list as staff only for non-superusers
            return User.objects.all().filter(is_staff=True).select_related()
    if db_field.name == "mentor":
        if request.user.is_superuser:
            return User.objects.all().select_related()
        else:
            return User.objects.all().filter().select_related()
    return None
#EndDef

# Now register ALL of our ModelAdmins with the admin.site
admin.site.register(Department, DepartmentAdmin)
admin.site.register(Course, CourseAdmin)
admin.site.register(Instructor, InstructorAdmin)
admin.site.register(Mentor, MentorAdmin)
admin.site.register(Enrollment, EnrollmentAdmin)
admin.site.register(Assignment, AssignmentAdmin)
admin.site.register(DueDateOverride, DueDateOverrideAdmin)
admin.site.register(Submission, SubmissionAdmin)
admin.site.register(Grade, GradeAdmin)
admin.site.register(ExtraCredit, ExtraCreditAdmin)
admin.site.register(Information, InformationAdmin)
admin.site.register(Resource, ResourceAdmin)
admin.site.register(Announcement, AnnouncementAdmin)



