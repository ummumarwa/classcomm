# encoding: utf-8
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):
    """
        SchemaMigration class for app student_portal -> model Enrollment.
        Move existing enrollment_length field to be called length_override field.
        
    """
    
    def forwards(self, orm):
        db.rename_column('student_portal_enrollment', 'enrollment_length', 'length_override')
    # EndDef

    def backwards(self, orm):
        db.rename_column('student_portal_enrollment', 'length_override', 'enrollment_length')
    # EndDef
# EndClass

