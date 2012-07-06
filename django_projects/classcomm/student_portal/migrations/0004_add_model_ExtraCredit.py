# encoding: utf-8
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models

class Migration(SchemaMigration):

    def forwards(self, orm):
        
        # Adding model 'ExtraCredit'
        db.create_table('student_portal_extracredit', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('return_date', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=100)),
            ('enrollment', self.gf('django.db.models.fields.related.ForeignKey')(related_name='ec_enrollment', to=orm['student_portal.Enrollment'])),
            ('points_earned', self.gf('django.db.models.fields.DecimalField')(max_digits=5, decimal_places=2)),
            ('comments', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
        ))
        db.send_create_signal('student_portal', ['ExtraCredit'])


    def backwards(self, orm):
        
        # Deleting model 'ExtraCredit'
        db.delete_table('student_portal_extracredit')


    models = {
        'auth.group': {
            'Meta': {'object_name': 'Group'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '80'}),
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
            'date_joined': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '75', 'blank': 'True'}),
            'first_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'groups': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.Group']", 'symmetrical': 'False', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'is_staff': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'is_superuser': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'last_login': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'last_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'password': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'user_permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.Permission']", 'symmetrical': 'False', 'blank': 'True'}),
            'username': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '30'})
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
            'author': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['auth.User']", 'null': 'True', 'blank': 'True'}),
            'content': ('django.db.models.fields.TextField', [], {}),
            'course': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'announcement_course'", 'null': 'True', 'to': "orm['student_portal.Course']"}),
            'department': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'announcement_department'", 'null': 'True', 'to': "orm['student_portal.Department']"}),
            'headline': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'make_global': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'pub_date': ('django.db.models.fields.DateTimeField', [], {'blank': 'True'})
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
            'points_possible': ('django.db.models.fields.IntegerField', [], {'default': '20'}),
            'provided_files': ('classcomm.student_portal.fields.ProtectedFileField', [], {'max_length': '250', 'null': 'True', 'blank': 'True'}),
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
            'name': ('django.db.models.fields.CharField', [], {'max_length': '150'})
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
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'length_override': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'mentor': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'enrollment_mentor'", 'null': 'True', 'to': "orm['auth.User']"}),
            'start_date': ('django.db.models.fields.DateField', [], {}),
            'student': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'enrollment_student'", 'to': "orm['auth.User']"})
        },
        'student_portal.extracredit': {
            'Meta': {'object_name': 'ExtraCredit'},
            'comments': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'enrollment': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'ec_enrollment'", 'to': "orm['student_portal.Enrollment']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'points_earned': ('django.db.models.fields.DecimalField', [], {'max_digits': '5', 'decimal_places': '2'}),
            'return_date': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'})
        },
        'student_portal.grade': {
            'Meta': {'object_name': 'Grade'},
            'assignment': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'grade_assignment'", 'to': "orm['student_portal.Assignment']"}),
            'comments': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'enrollment': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'grade_enrollment'", 'to': "orm['student_portal.Enrollment']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'points_earned': ('django.db.models.fields.DecimalField', [], {'max_digits': '5', 'decimal_places': '2'}),
            'return_date': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'returned_files': ('classcomm.student_portal.fields.ProtectedFileField', [], {'max_length': '250', 'null': 'True', 'blank': 'True'})
        },
        'student_portal.information': {
            'Meta': {'object_name': 'Information'},
            'course': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'info_course'", 'null': 'True', 'to': "orm['student_portal.Course']"}),
            'department': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'info_department'", 'null': 'True', 'to': "orm['student_portal.Department']"}),
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
            'course': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'resource_course'", 'null': 'True', 'to': "orm['student_portal.Course']"}),
            'department': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'resource_department'", 'null': 'True', 'to': "orm['student_portal.Department']"}),
            'details': ('django.db.models.fields.TextField', [], {}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'url': ('django.db.models.fields.CharField', [], {'max_length': '200', 'null': 'True', 'blank': 'True'})
        },
        'student_portal.submission': {
            'Meta': {'object_name': 'Submission'},
            'add_checkscript': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'assignment': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['student_portal.Assignment']"}),
            'date': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'enrollment': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['student_portal.Enrollment']"}),
            'file': ('classcomm.student_portal.fields.ProtectedFileField', [], {'max_length': '250'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'on_time': ('django.db.models.fields.BooleanField', [], {'default': 'True'})
        }
    }

    complete_apps = ['student_portal']
