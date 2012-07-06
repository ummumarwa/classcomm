# Python Script for generating a random valid SECRET_KEY for Django project settings.py file.

import string
from random import choice

print ''.join([choice(string.letters + string.digits + string.punctuation) for i in range(50)])
