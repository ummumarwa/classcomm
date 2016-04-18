# Currently Bundled Extensions #

Currently classcomm is bundled with and expands upon third party open source apps to improve the vision of what classcomm can be.  These apps do not need to be installed extra because we include our own customized version in the Classcomm-Django project.
  * [django\_debug\_toolbar](https://github.com/robhudson/django-debug-toolbar) - Unmodified release of version 0.8.4.  Provides Enhanced Debuging Data for Django and Classcomm.
  * [django-registration](http://bitbucket.org/ubernostrum/django-registration/) - Self-Modified branch on release of version 0.8.  This app was used as the base for what is now classcomm.registration.  Plans include opening accounts authentication up to Facebook, Twitter and OpenID with the right connectors for .
  * [django-south](http://south.aeracode.org/) - Unmodified South 0.7.3 is now included in project for handling schema migrations.  This has been useful for rolling out schema migrations changes to already deployed versions, and also for rolling them back at points of failures and testing new features.  This tool should be used in conjunction with another tool for databases introspection and (possibly modifcation) such as phpMyAdmin or phpPostgresAdmin.  So far, all my testing has done in MySQL--plans are a-rye for testing with PostgresSQL, and also testing load capacities using a tool such as flood.  See also page on [Django Schema Evolution](http://code.djangoproject.com/wiki/SchemaEvolution) for discussion; See also SchemaChanges for more information on using south with classcomm.

## Approved Developer Add-On Tools (Not Bundled) ##
  * [django-command-extensions](https://github.com/django-extensions/django-extensions/) -- The main thing I like so far from this package is the ability to generate png image files of the entire project's Model Layout.  This is a really useful feature that I've been looking out for since the start of the project.
  * [django-output-validator](http://pypi.python.org/pypi/django-output-validator/) For validating all HTML generated in a Django Development Environment.  For more information see wiki document on TestingStrategies

## Approved Classcomm Extension (Not Bundled) ##
  * [django-sentry](https://github.com/dcramer/django-sentry) for providing a dashboard and view panel for the deployed instance logging and Exceptions.  Also supports interfacing with other Sentry clients on the network.  **Does not seem to be working in latest Django 1.3 Beta so we have it disabled.
  * [overseer](https://github.com/disqus/overseer) -- Overseer is a status board app written in Django.  So far it has no support for automated service monitoring but instead offers a service status board with Events and Updates configurable in the Admin when this extension is installed.  Unfortunately it makes it more difficult to bundle since it requires python-oauth2 which is not a standard package.  Due to the limited nature of this App and the extra requirements it is not bundled standard at this time, but we believe it will fulfill goals of some users.**

# Research on Third-Parties #

Evaluating existing open source Third-Party Apps, Extensions and other Projects for possible integration with our project and our development culture is a major focus and will help us reach our goals sooner rather than later.  Also this practice will inspire other developers to improve upon their existing products as well as prevent us from reinventing the wheel.  We maintain a high bar of quality for accepted projects: it must target one of our current core goals, provide features that aren't too expensive using technologies that aren't too experimental and are inline with our existing infrastructure.

## Research In Motion (Current) ##
  * [django-locking](http://stdbrouw.github.com/django-locking/design.html) For adding editor locks across  of locking to database transactions.  Well this is of interest for the minor concurrency race condition we have today for parallel systems.  What we need ideally is User level locking where every qualifying model gets their own lock with an expiry timeout.
  * [django-admin-tools](https://bitbucket.org/izi/django-admin-tools/wiki/Home) - The Django-Admin-Tools package allows customization of the admin by adding links and pannels to custom views, and customizing the interface.
  * [django-quiz](https://github.com/myles/django-quiz) - This intends to be a quiz style app for Django.  We may use this as the basis for clascomm-quizes.
  * [uuidfield](https://github.com/dcramer/django-uuidfield)  -- This adds a Unique Identifier Field to Django to be used as model field.
  * [gargoyle](https://github.com/disqus/gargoyle) -- Gargoyle is a platform built on top of Django which allows you to switch functionality of your application on and off based on conditions.  Could be a useful option for allowing the end user higher customization of the UI and feature-set.
  * [facebook-python-sdk](https://github.com/disqus/facebook-python-sdk) -- Library for authenticating against Facebook in Python.
  * [johny-cache](http://packages.python.org/johnny-cache/index.html) -- "It works with the django caching abstraction, but was developed specifically with the use of memcached in mind. Its main feature is a patch on Django’s ORM that automatically caches all reads in a consistent manner."
  * [django-revision](http://code.google.com/p/django-reversion/) - A tool for tracking changes to Django Models.  Here is a [Blog Post](http://blog.brunogola.com.br/2009/10/django-model-history-with-django-reversion/) about Django-Revision.
  * [fullhistory](http://code.google.com/p/fullhistory/) - A tool for tracking changes to Django Models.  Presently it looks like Django-Revision is a better supported tool.

## Future Research ##
  * [django-livesettings](https://bitbucket.org/bkroeze/django-livesettings/) Supports editing django settings in the admin interface.
  * [django-ajax-selects](http://code.google.com/p/django-ajax-selects/) Provide the Django Admin interface with lookup-as-you-type AJAX for ForeignKey fields.
  * [django-html5](https://github.com/rhec/django-html5) This library intends to extend Django support with HTML5 widgets and other goodies.  I'm not sure what this means or that such a thing would even be necessary, but you never know.
  * [django-cache-machine](https://github.com/jbalogh/django-cache-machine) -- "Cache Machine provides automatic caching and invalidation for Django models through the ORM."  Both this an
  * Django-Google-Analytics
  * Django-SITEMETRICS
  * [django-chronograph](http://code.google.com/p/django-chronograph/) - By the same guy that does Django-genericadmin, this seems to install a cron like interface to Django allowing you configure jobs within the Django admin.  Maybe will prove useful on some of our future plugin apps.
  * [Cloud Couse](http://code.google.com/p/cloudcourse/) - This Existing Django Project is a Course Scheduling System Built entirely on App Engine, CloudCourse allows anyone to create and track learning activities. It also offers calendaring, waitlist management and approval features.  Now the Django is being supported by app engine, We want to deploy and try out this code base and determine from there what benefits it could bring to classcomm as a possibly integration pathway.


## Old Research (Tried, read and reviewed) ##
  * [Grappelli installation instructions django-grappelli](http://code.google.com/p/django-grappelli/wiki/Installation_2_2) - Grappelli is a new skin for the Django admin.  I installed this on a VirtualBox instance of classcomm to try it out.  It is basicaly an attractive reskinned admin.  We may consider at some point packaging with this in trunk and making it an option to Users or some other integration pathway.
  * [django-guardian](http://packages.python.org/django-guardian/configuration.html) - Allows extending Django permissions system.  The problem is this assumes a different permissions model that the one we've implemented.  We don't really want to limit users to certain subsets of data in the admin and this seems to address more global Object properties.
  * [django-genericadmin](http://code.google.com/p/django-genericadmin/) - Admin Enhancement (??) for Generic Relations in Django.  We have tested migrating the Information schema in South to make some of our objects generic.  My gut reaction is that generic relations are still at Django 1.3 poorly supported at best.  They seem to complicate the logical structure of the code without providing any real useful UI to use them with.  I will say that even with the proper UI that generic relations in Django should be left for things like a site wide pluggable comments app.


## Other Interesting Projects (Django or Related) ##

[django-pluggables](https://github.com/nowells/django-pluggables#readme) is a Django design pattern for making pluggable apps available within a project (one example: a pluggable comments system) well certainly a good idea, and out of the box you can make an app available at different URLS.

[Django Evolution](http://code.google.com/p/django-evolution/) is a Schema migration tools similar to **South (our alternative)** for Django.  However at this point in development South seems to have better features/less bugs.  However we may want to keep an eye out as this project develops.

[Django-photologue](http://code.google.com/p/django-photologue/) - Django Photo Library with gallery support.

[Celery](http://celeryq.org/docs/django-celery/getting-started/first-steps-with-django.html#special-note-for-mod-wsgi-users) - Celery is an asynchronous task queue/job queue based on distributed message passing. It is focused on real-time operation, but supports scheduling as well.  The execution units, called tasks, are executed concurrently on a single or more worker servers. Tasks can execute asynchronously (in the background) or synchronously (wait until ready).  This could be useful in scaling our Django project, for having more powerful computations done on external hosts and have the Django site pass the work onto those servers and get the results back to render the pages.  Obviously there are trade-offs here, and presently we do not have work units appropriate enough for this.

[redis](http://code.google.com/p/redis/) is a persistent key-value database with built-in net interface written in ANSI-C for Posix systems.  It has support for all popular languages and is one of two supported systems for use with Celery as a messaging agent.  The other being [RabbitMQ](http://www.rabbitmq.com/faq.html#what-is-messaging)

[Django Excel Templates](http://code.google.com/p/django-excel-templates/) - This project aims to make generating Excel documents from within Django a breeze.  We may want to include this at a stable release point for generating Excel documents.

[Kay Framework](http://code.google.com/p/kay-framework/) - This is a framework based on Django for running specificaly in the Google App Engine Environment.  Doubtful this will be of much use to use, but if we build part of our deployments around Google App Engine, then perhaps this will be of some use.

[Django Blocks](http://code.google.com/p/django-blocks/) - Is an extension of the Django Framework for creating content.  We may want to check back on this at some point to see if any valuable ideas can be gleamed from their work.

[Dango Modified Preorder Tree Traversal](http://code.google.com/p/django-mptt/) - Utilities for implementing Modified Preorder Tree Traversal.

[Django Projector](http://www.django-projector.org/) - Open Source Project Management System/App with repository back-end support.  So far does not support subversion (only git and mercureal) but the design seems light weight and powerful despite some bugs and initial flaws.

[Unfuddle](http://unfuddle.com/) is another project hosting site that supports tickets, SVN and git code hosting.

[Stack Overflow Clone](http://code.google.com/p/soclone/) - A Django project that tire to implement stack overflow for internal company deployments.

[DSE](https://bitbucket.org/weholt/dse2/src) - This is intended to replace the Django ORM for executing queries and is believed to greatly improve query performance when the number of DB entries to be operated on exceeded 100,000.


## Addendums (Other Listings) ##
[Django Advent 2.1 2010](http://djangoadvent.com/1.2/django-template-improvements/)
20 Days, every day is an article written by someone else about an improvement with Django 1.2 and onto including 1.3.   Of varying quality, I definitely believe the django-template-improvements are going to make a difference when I go to do capacity benchmarks.
[Django Con 2010 Listing](http://jeffammons.net/2010/09/popular-django-apps-at-djangocon-2010/) Another less annotated list of projects.