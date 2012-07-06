# encoding: utf-8
from south.db import db
from south.v2 import SchemaMigration
from django.db import models
from datetime import datetime


class Migration(SchemaMigration):
    """
        SchemaMigration class 0004 for app student_portal -> model Grade.
        Add table column for the date the Grade object is created (day student received grade).

    """

    def forwards(self, orm):
        """ Adding column return_date in Model Grade. """
        db.add_column('student_portal_grade', 'return_date', models.DateTimeField(default=datetime.today()))
    # EndDef

    def backwards(self, orm):
        """ Deleting column return_date in Model Grade. """
        db.delete_column('student_portal_grade', 'return_date')
    # EndDef
# EndClass

