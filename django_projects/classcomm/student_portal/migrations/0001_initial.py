# encoding: utf-8
from south.db import db
from south.v2 import SchemaMigration
from django.db import models
from datetime import datetime


class Migration(SchemaMigration):

    def forwards(self, orm):
        
        # Adding model 'Department'
        db.create_table('student_portal_department', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=100)),
        ))
        db.send_create_signal('student_portal', ['Department'])

        # Adding model 'Course'
        db.create_table('student_portal_course', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('department', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['student_portal.Department'])),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=100)),
            ('director', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['auth.User'], null=True, blank=True)),
            ('open_enrollments', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('enrollment_length', self.gf('django.db.models.fields.IntegerField')(default=16)),
            ('description', self.gf('django.db.models.fields.TextField')()),
        ))
        db.send_create_signal('student_portal', ['Course'])

        # Adding model 'Instructor'
        db.create_table('student_portal_instructor', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('course', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['student_portal.Course'])),
            ('instructor', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['auth.User'])),
        ))
        db.send_create_signal('student_portal', ['Instructor'])

        # Adding model 'Mentor'
        db.create_table('student_portal_mentor', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('course', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['student_portal.Course'])),
            ('mentor', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['auth.User'])),
        ))
        db.send_create_signal('student_portal', ['Mentor'])

        # Adding model 'Enrollment'
        db.create_table('student_portal_enrollment', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('student', self.gf('django.db.models.fields.related.ForeignKey')(related_name='student_enrollment', to=orm['auth.User'])),
            ('course', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['student_portal.Course'])),
            ('start_date', self.gf('django.db.models.fields.DateField')()),
            ('enrollment_length', self.gf('django.db.models.fields.IntegerField')(null=True, blank=True)),
            ('access_mode', self.gf('django.db.models.fields.CharField')(default='Normal', max_length=15)),
            ('mentor', self.gf('django.db.models.fields.related.ForeignKey')(related_name='mentor_enrollment', blank=True, null=True, to=orm['auth.User'])),
        ))
        db.send_create_signal('student_portal', ['Enrollment'])

        # Adding model 'Assignment'
        db.create_table('student_portal_assignment', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('course', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['student_portal.Course'])),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=200)),
            ('details', self.gf('django.db.models.fields.TextField')()),
            ('points_possible', self.gf('django.db.models.fields.IntegerField')(default=0)),
            ('display_points_possible', self.gf('django.db.models.fields.BooleanField')(default=True)),
            ('provided_files', self.gf('django.db.models.fields.files.FileField')(max_length=100, null=True, blank=True)),
            ('apply_due_date', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('weeks_after', self.gf('django.db.models.fields.IntegerField')(default=0)),
            ('days_after', self.gf('django.db.models.fields.IntegerField')(default=0)),
            ('allow_late', self.gf('django.db.models.fields.BooleanField')(default=True)),
            ('disable_submissions', self.gf('django.db.models.fields.BooleanField')(default=False)),
        ))
        db.send_create_signal('student_portal', ['Assignment'])

        # Adding model 'DueDateOverride'
        db.create_table('student_portal_duedateoverride', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('enrollment', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['student_portal.Enrollment'])),
            ('assignment', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['student_portal.Assignment'])),
            ('weeks_after', self.gf('django.db.models.fields.IntegerField')(default=0)),
            ('days_after', self.gf('django.db.models.fields.IntegerField')(default=0)),
            ('allow_late', self.gf('django.db.models.fields.BooleanField')(default=True)),
        ))
        db.send_create_signal('student_portal', ['DueDateOverride'])

        # Adding model 'Submission'
        db.create_table('student_portal_submission', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('enrollment', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['student_portal.Enrollment'])),
            ('assignment', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['student_portal.Assignment'])),
            ('date', self.gf('django.db.models.fields.DateTimeField')()),
            ('file', self.gf('django.db.models.fields.files.FileField')(max_length=100)),
            ('on_time', self.gf('django.db.models.fields.BooleanField')(default=True)),
            ('add_checkscript', self.gf('django.db.models.fields.BooleanField')(default=True)),
        ))
        db.send_create_signal('student_portal', ['Submission'])

        # Adding model 'Grade'
        db.create_table('student_portal_grade', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('enrollment', self.gf('django.db.models.fields.related.ForeignKey')(related_name='enrollment_grade', to=orm['student_portal.Enrollment'])),
            ('assignment', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['student_portal.Assignment'])),
            ('points_earned', self.gf('django.db.models.fields.DecimalField')(max_digits=5, decimal_places=2)),
            ('returned_files', self.gf('django.db.models.fields.files.FileField')(max_length=100, null=True, blank=True)),
            ('comments', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
        ))
        db.send_create_signal('student_portal', ['Grade'])

        # Adding model 'Resource'
        db.create_table('student_portal_resource', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('department', self.gf('django.db.models.fields.related.ForeignKey')(related_name='department_resource', blank=True, null=True, to=orm['student_portal.Department'])),
            ('course', self.gf('django.db.models.fields.related.ForeignKey')(related_name='course_resource', blank=True, null=True, to=orm['student_portal.Course'])),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=100)),
            ('url', self.gf('django.db.models.fields.CharField')(max_length=200, null=True, blank=True)),
            ('details', self.gf('django.db.models.fields.TextField')()),
        ))
        db.send_create_signal('student_portal', ['Resource'])

        # Adding model 'Information'
        db.create_table('student_portal_information', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('department', self.gf('django.db.models.fields.related.ForeignKey')(related_name='department_info', blank=True, null=True, to=orm['student_portal.Department'])),
            ('course', self.gf('django.db.models.fields.related.ForeignKey')(related_name='course_info', blank=True, null=True, to=orm['student_portal.Course'])),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=100)),
            ('description', self.gf('django.db.models.fields.CharField')(max_length=200)),
            ('details', self.gf('django.db.models.fields.TextField')()),
        ))
        db.send_create_signal('student_portal', ['Information'])

        # Adding model 'Announcement'
        db.create_table('student_portal_announcement', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('make_global', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('department', self.gf('django.db.models.fields.related.ForeignKey')(related_name='department_announcement', blank=True, null=True, to=orm['student_portal.Department'])),
            ('course', self.gf('django.db.models.fields.related.ForeignKey')(related_name='course_announcement', blank=True, null=True, to=orm['student_portal.Course'])),
            ('author', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['auth.User'])),
            ('pub_date', self.gf('django.db.models.fields.DateTimeField')()),
            ('headline', self.gf('django.db.models.fields.CharField')(max_length=100)),
            ('content', self.gf('django.db.models.fields.TextField')()),
        ))
        db.send_create_signal('student_portal', ['Announcement'])


    def backwards(self, orm):
        
        # Deleting model 'Department'
        db.delete_table('student_portal_department')

        # Deleting model 'Course'
        db.delete_table('student_portal_course')

        # Deleting model 'Instructor'
        db.delete_table('student_portal_instructor')

        # Deleting model 'Mentor'
        db.delete_table('student_portal_mentor')

        # Deleting model 'Enrollment'
        db.delete_table('student_portal_enrollment')

        # Deleting model 'Assignment'
        db.delete_table('student_portal_assignment')

        # Deleting model 'DueDateOverride'
        db.delete_table('student_portal_duedateoverride')

        # Deleting model 'Submission'
        db.delete_table('student_portal_submission')

        # Deleting model 'Grade'
        db.delete_table('student_portal_grade')

        # Deleting model 'Resource'
        db.delete_table('student_portal_resource')

        # Deleting model 'Information'
        db.delete_table('student_portal_information')

        # Deleting model 'Announcement'
        db.delete_table('student_portal_announcement')


    models = {
        'auth.group': {
            'Meta': {'object_name': 'Group'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '80', 'unique': 'True'}),
            'permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.Permission']", 'symmetrical': 'False', 'blank': 'True'})
        },
        'auth.permission': {
            'Meta': {'ordering': "('content_type__app_label', 'content_type__model', 'codename')", 'unique_together': "(('content_type', 'codename'),)", 'object_name': 'Permission'},
            'codename': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'content_type': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['contenttypes.ContentType']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        },
        'auth.user': {
            'Meta': {'object_name': 'User'},
            'date_joined': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.now'}),
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '75', 'blank': 'True'}),
            'first_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'groups': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.Group']", 'symmetrical': 'False', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'is_staff': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'is_superuser': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'last_login': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.now'}),
            'last_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'password': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'user_permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.Permission']", 'symmetrical': 'False', 'blank': 'True'}),
            'username': ('django.db.models.fields.CharField', [], {'max_length': '30', 'unique': 'True'})
        },
        'contenttypes.contenttype': {
            'Meta': {'ordering': "('name',)", 'unique_together': "(('app_label', 'model'),)", 'object_name': 'ContentType', 'db_table': "'django_content_type'"},
            'app_label': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'model': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        'student_portal.announcement': {
            'Meta': {'object_name': 'Announcement'},
            'author': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['auth.User']"}),
            'content': ('django.db.models.fields.TextField', [], {}),
            'course': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'course_announcement'", 'blank': 'True', 'null': 'True', 'to': "orm['student_portal.Course']"}),
            'department': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'department_announcement'", 'blank': 'True', 'null': 'True', 'to': "orm['student_portal.Department']"}),
            'headline': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'make_global': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'pub_date': ('django.db.models.fields.DateTimeField', [], {})
        },
        'student_portal.assignment': {
            'Meta': {'object_name': 'Assignment'},
            'allow_late': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'apply_due_date': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'course': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['student_portal.Course']"}),
            'days_after': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'details': ('django.db.models.fields.TextField', [], {}),
            'disable_submissions': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'display_points_possible': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            'points_possible': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'provided_files': ('django.db.models.fields.files.FileField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'weeks_after': ('django.db.models.fields.IntegerField', [], {'default': '0'})
        },
        'student_portal.course': {
            'Meta': {'object_name': 'Course'},
            'department': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['student_portal.Department']"}),
            'description': ('django.db.models.fields.TextField', [], {}),
            'director': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['auth.User']", 'null': 'True', 'blank': 'True'}),
            'enrollment_length': ('django.db.models.fields.IntegerField', [], {'default': '16'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'open_enrollments': ('django.db.models.fields.BooleanField', [], {'default': 'False'})
        },
        'student_portal.department': {
            'Meta': {'object_name': 'Department'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        'student_portal.duedateoverride': {
            'Meta': {'object_name': 'DueDateOverride'},
            'allow_late': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'assignment': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['student_portal.Assignment']"}),
            'days_after': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'enrollment': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['student_portal.Enrollment']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'weeks_after': ('django.db.models.fields.IntegerField', [], {'default': '0'})
        },
        'student_portal.enrollment': {
            'Meta': {'object_name': 'Enrollment'},
            'access_mode': ('django.db.models.fields.CharField', [], {'default': "'Normal'", 'max_length': '15'}),
            'course': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['student_portal.Course']"}),
            'enrollment_length': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'mentor': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'mentor_enrollment'", 'blank': 'True', 'null': 'True', 'to': "orm['auth.User']"}),
            'start_date': ('django.db.models.fields.DateField', [], {}),
            'student': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'student_enrollment'", 'to': "orm['auth.User']"})
        },
        'student_portal.grade': {
            'Meta': {'object_name': 'Grade'},
            'assignment': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['student_portal.Assignment']"}),
            'comments': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'enrollment': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'enrollment_grade'", 'to': "orm['student_portal.Enrollment']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'points_earned': ('django.db.models.fields.DecimalField', [], {'max_digits': '5', 'decimal_places': '2'}),
            'returned_files': ('django.db.models.fields.files.FileField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'})
        },
        'student_portal.information': {
            'Meta': {'object_name': 'Information'},
            'course': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'course_info'", 'blank': 'True', 'null': 'True', 'to': "orm['student_portal.Course']"}),
            'department': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'department_info'", 'blank': 'True', 'null': 'True', 'to': "orm['student_portal.Department']"}),
            'description': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            'details': ('django.db.models.fields.TextField', [], {}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        'student_portal.instructor': {
            'Meta': {'object_name': 'Instructor'},
            'course': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['student_portal.Course']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'instructor': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['auth.User']"})
        },
        'student_portal.mentor': {
            'Meta': {'object_name': 'Mentor'},
            'course': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['student_portal.Course']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'mentor': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['auth.User']"})
        },
        'student_portal.resource': {
            'Meta': {'object_name': 'Resource'},
            'course': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'course_resource'", 'blank': 'True', 'null': 'True', 'to': "orm['student_portal.Course']"}),
            'department': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'department_resource'", 'blank': 'True', 'null': 'True', 'to': "orm['student_portal.Department']"}),
            'details': ('django.db.models.fields.TextField', [], {}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'url': ('django.db.models.fields.CharField', [], {'max_length': '200', 'null': 'True', 'blank': 'True'})
        },
        'student_portal.submission': {
            'Meta': {'object_name': 'Submission'},
            'add_checkscript': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'assignment': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['student_portal.Assignment']"}),
            'date': ('django.db.models.fields.DateTimeField', [], {}),
            'enrollment': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['student_portal.Enrollment']"}),
            'file': ('django.db.models.fields.files.FileField', [], {'max_length': '100'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'on_time': ('django.db.models.fields.BooleanField', [], {'default': 'True'})
        }
    }

    complete_apps = ['student_portal']

