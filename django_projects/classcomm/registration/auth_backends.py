from django.db import connection
from django.contrib.auth.models import User, Permission
from django.contrib.auth.backends import ModelBackend

class ModelBackendEmail(ModelBackend):
    """
    Authenticates against django.contrib.auth.models.User
    using the E-mail as opposed to the username as does ModelBackend
    """
    def authenticate(self, username=None, password=None):
        try:
            user = User.objects.get(email=username)
            if user.check_password(password):
                return user
        except User.DoesNotExist:
            return None

