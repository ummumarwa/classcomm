"""
URLconf for registration and activation, using django-registration's
default backend `django.contrib.auth`.

We use a line like this in root URLconf to set up the default URLs
for registration::

   (r'^registration/', include('registration.backends.default.urls')),
   

We may want to customize the behavior (e.g., by passing extra
arguments to the various views) or split up the URLs or add
additional pages to our registration backend system.

We will add URLs for resending/regenerating activation keys here as well.
"""


from django.conf.urls.defaults import *
from django.views.generic.simple import direct_to_template

from registration.views import activate
from registration.views import register
from registration.views import resend


urlpatterns = patterns('',
                       url(r'^activate/complete/$',
                           direct_to_template,
                           { 'template': 'registration/activation_complete.html' },
                           name='registration_activation_complete'),
                       # Activation keys get matched by \w+ instead of the more specific
                       # [a-fA-F0-9]{40} because a bad activation key should still get to the view;
                       # that way it can return a sensible "invalid key" message instead of a
                       # confusing 404.
                       url(r'^activate/(?P<activation_key>\w+)/$',
                           activate,
                           { 'backend': 'registration.backends.default.DefaultBackend' },
                           name='registration_activate'),
                       url(r'^register/$',
                           register,
                           { 'backend': 'registration.backends.default.DefaultBackend' },
                           name='registration_register'),
                       url(r'^resend/$',
                           resend,
                           { 'backend': 'registration.backends.default.DefaultBackend' },
                           name='registration_resend'),
                       url(r'^register/complete/$',
                           direct_to_template,
                           { 'template': 'registration/registration_complete.html' },
                           name='registration_complete'),
                       url(r'^register/closed/$',
                           direct_to_template,
                           { 'template': 'registration/registration_closed.html' },
                           name='registration_disallowed'),
                       (r'', include('registration.auth_urls')),
                       )
