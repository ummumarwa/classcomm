"""
    File for custom DB Fields for our app. Now we replace replace FileField with subclassed ProtectedFileField
     with no schema change.  Our subclass defined below uses gen_sec_link to generate secure time expiring links.
     If another security mechanism were implemented to protect files it would likely be implemented here.

"""

from django.conf import settings    # Make Classcomm AUTH_TOKEN_PASSWORD setting available
import hashlib                      # Import encryption library
import time                         # Date related functionality
from django.db.models.fields.files import *
from south.modelsinspector import add_introspection_rules

# We need to add introspection rules to our custom fields for Django-South to function properly.
add_introspection_rules([], ["^classcomm\.student_portal\.fields\.ProtectedFileField"])


def gen_sec_link(rel_path):
    """
    Generate a temporary authorized link to download a file @param rel_path.
    This function is used with Apache mod_auth_token to serve up secure content.
    
    """
    secret = settings.AUTH_TOKEN_PASSWORD
    uri_prefix = '/media/uploads/'
    rel_path = rel_path[7:]
    hextime = "%08x" % time.time()
    token = hashlib.md5(secret + rel_path + hextime).hexdigest()
    return '%s%s/%s%s' % (uri_prefix, token, hextime, rel_path)
# EndDef

class ProtectedFieldFile(FieldFile):
    """
    This subclass of FieldFile (which is FileField's underlying storage class)
    overrides the url API method to implement mod_auth_token secure links for all ProtectedFileFields.
    Reason this is great: it fixes all broken links in applications that use this models.file_field.url and
        allows the template language to be simplified and less prone to errors.

    """
    def _get_url(self):
        self._require_file()
        return gen_sec_link(self.name)
    url = property(_get_url)
# EndClass

class ProtectedFileField(FileField):
    """
    This class class is the model field label you would declare in models.py
    
    """
    attr_class = ProtectedFieldFile
    description = ugettext_lazy("File path with Auth_Token support.")
# EndClass

