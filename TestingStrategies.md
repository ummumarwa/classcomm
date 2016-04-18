# Running Tests #
This section is incomplete.  Will update with the release of Django 1.3 and updated fixed tests committed.

## unittest(2) ##
Currently the level of testing varies across the classcomm project app-space, but the situation is improving.  The goal is to have



# Validating Generated Markup Pages #
2/26/2011 -- We have hit the milestone goal of automating our page validation thanks to the Django App written by [Luke Plant](http://lukeplant.me.uk/).

## Traditional Opera Approach ##
The traditional approach is to make minor changes or incremental code changes, and load the possibly page views in [Opera Web Browser](http://www.opera.com/), right-click and select validate which will submit the page to validator.w3.org.  The validator will find and highlight each markup error and developers will correct and retry.

## Automatic Page Validation with Error Reports ##
**NEW:** The Traditional Approach works great for verifying current code generates validate page markup (current target is XHTML strict) however the Traditional Approach is also very manual and time intensive.  We can add automated validation of every page we render on our development environment with aggregated error reports at the url\_path('/validator/') by dropping in [django-output-validator package](http://pypi.python.org/pypi/django-output-validator/#downloads) to our test-driven development environment.

**1.) Get the Django App django-output-validator and make it available on the Python Path:**
```
cd ~
wget http://pypi.python.org/packages/source/d/django-output-validator/django-output-validator-1.5.tar.gz#md5=b7d19e2bcb50b8dc076c6e8259150f57
tar xzvf django-output-validator-1.5.tar.gz
cd django-output-validator-1.5
sudo python setupy.py install
```

**2.) Edit our project's settings.py file and add several things:**
```
# In the Project Root ('/var/django_projects/classcomm/')
sudo vim settings.py

# Now add the following line to  your INSTALLED_APPS tupple:
"output_validator",

# Verify TEMPLATE_LOADERS tupple has the app_directories.loader:
"django.template.loaders.app_directories.Loader",

# Add the middleware to validate every generated request near the beginning of the middleware list but after GZip:
MIDDLEWARE_CLASSES = (
    'django.middleware.gzip.GZipMiddleware',
    'output_validator.middleware.ValidatorMiddleware',
    'django.middleware.common.CommonMiddleware',
    ....
)

# Add the following setting to the file:
OUTPUT_VALIDATOR_VALIDATORS = {
  'text/html': '/usr/bin/validate',
  'application/xml+xhtml': '/usr/bin/validate',
}
```

**3.) Now edit our project's urls.py file and add the validator reports urls:**
```
# In the Project Root ('/var/django_projects/classcomm/')
sudo vim urls.py

# The following line links in the generated validation error reports:
(r'^validator/', include('output_validator.urls'))
```

Currently we have to workaround [an issue](https://bugs.edge.launchpad.net/ubuntu/+source/w3c-dtd-xhtml/+bug/390604) with the default validator which installs from the default ubuntu repositories so we will give instructions on fixing this.  Once you have django-output-validator configured, we will need to install the actual local validator package from the [Debian repository](http://packages.debian.org/squeeze/all/w3c-dtd-xhtml/download).


**4.) We are almost there, but before our validation will work we need to get the working validator installed:**
```
cd ~
wget http://debian.oregonstate.edu/debian/pool/main/w/w3c-dtd-xhtml/w3c-dtd-xhtml_1.1-5_all.deb
sudo dpkg -i w3c-dtd-xhtml_1.1-5_all.deb
```

**OK, That should be it!**   Now you can use the website as you would in your development environment and every page view will be validated and you will only see items in your report when the page view fails validation.  You can also add a setting **OUTPUT\_VALIDATOR\_IGNORE\_PATHS** to bypass URL paths from validation such as:
```
OUTPUT_VALIDATOR_IGNORE_PATHS = [
    '/admin/',
    '/validator/',
]
```