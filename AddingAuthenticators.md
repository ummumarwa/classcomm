# Introduction #

By default, classcomm uses Djangos built in User class and requires that each new user be created in the Django admin.  However some networks already have user credentials in play so the fix django offers is chaining authenticators.  You may write your own authenticator knowing your network configuration.  Below are some examples of how to do this.


# Details #

In this example borrowed from [carthage](http://www.carthage.edu/webdev/?p=12) we see that
authentication chaining can takes place in the classcomm settings.py file:
```
AUTHENTICATION_BACKENDS = (
 'classcomm.backends.ldapBackend.LDAPBackend',
 'django.contrib.auth.backends.ModelBackend',
)
```
which that file classcomm.backends.ldapBackend would look something like
```
import ldap
from django.contrib.auth.models import User

# Constants
AUTH_LDAP_SERVER = 'Your LDAP Server'
AUTH_LDAP_BASE_USER = "cn=Your, o=BaseUser"
AUTH_LDAP_BASE_PASS = "Your Base Password"

class LDAPBackend:
    def authenticate(self, username=None, password=None):
        base = "o=YourOrganization"
        scope = ldap.SCOPE_SUBTREE
        filter = "(&(objectclass=person) (cn=%s))" % username
        ret = ['dn']

        # Authenticate the base user so we can search
        try:
            l = ldap.open(AUTH_LDAP_SERVER)
            l.protocol_version = ldap.VERSION3
            l.simple_bind_s(AUTH_LDAP_BASE_USER,AUTH_LDAP_BASE_PASS)
        except ldap.LDAPError:
            return None

        try:
            result_id = l.search(base, scope, filter, ret)
            result_type, result_data = l.result(result_id, 0)

            # If the user does not exist in LDAP, Fail.
            if (len(result_data) != 1):
                return None

            # Attempt to bind to the user's DN
            l.simple_bind_s(result_data[0][0],password)

            # The user existed and authenticated. Get the user
            # record or create one with no privileges.
            try:
                user = User.objects.get(username__exact=username)
            except:
                # Theoretical backdoor could be input right here. We don't
                # want that, so input an unused random password here.
                # The reason this is a backdoor is because we create a
                # User object for LDAP users so we can get permissions,
                # however we -don't- want them able to login without
                # going through LDAP with this user. So we effectively
                # disable their non-LDAP login ability by setting it to a
                # random password that is not given to them. In this way,
                # static users that don't go through ldap can still login
                # properly, and LDAP users still have a User object.
                from random import choice
                import string
                temp_pass = ""
                for i in range(8):
                    temp_pass = temp_pass + choice(string.letters)
                user = User.objects.create_user(username,
                         username + '@carthage.edu',temp_pass)
                user.is_staff = False
                user.save()
            # Success.
            return user
           
        except ldap.INVALID_CREDENTIALS:
            # Name or password were bad. Fail.
            return None

    def get_user(self, user_id):
        try:
            return User.objects.get(pk=user_id)
        except User.DoesNotExist:
            return None
```