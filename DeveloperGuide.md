# Classcomm Code #

Classcomm uses a Google Code [Subversion](http://subversion.tigris.org/) repository for source control, and  On Windows 7, the best interface to Subversion is the [Tortoise SVN](http://tortoisesvn.tigris.org/) shell extensions which allow you to work with code repositories within windows explorer with nice straightforward working GUI extensions.


# Quality Development Tools #

Classcomm is a [Django Project](http://djangoproject.org/) and on Windows the best Python IDE with Django support seems to be [JetBrains PyCharm](http://www.jetbrains.com/pycharm/) and they have graciously granted free open source licenses to open source projects in the past.

[JS Lint](http://jslint.com/) is a Java Script a quality control tool written by Douglas Crockford who gave [this Google Con presentation](http://www.youtube.com/watch?v=hQVTIJBZook) on the reason why so many people end up writing bad Java Script.  Doug also developed the [JSON Standard](http://json.org/) which classcomm developers should use for any AJAX-server call-back work or really as an alternative to XML.

[phpMyAdmin](https://help.ubuntu.com/community/phpMyAdmin) is recommended for deployment to classcomm to help verify and in rare instances fine tune your working database.  Django afterall is a software tool that makes it easier to interact with a Database--It is not a Database Admin Tool in and of itself.  This niche has been filled successfully by phpMyAdmin and will play nicely with your already Apache deployed Django-Classcomm.  The Ubuntu phpMyAdmin installer also has the option to deploy the lighttpd server which is an optional pathway.  Just now I used phpMyAdmin to remove a couple columns from a database table that were breaking my development app.

Of course FireBug in FireFox, the Django Debug Toolbar and CSS validation in Opera are also useful and beautiful tools.

[Googlebot Spoofer](http://www.smart-it-consulting.com/internet/google/googlebot-spoofer/)



# Virtual Box #

Classcomm trunk repository is approaching the stability of largely available package releases.  One method of testing classcomm privately and trying some test driven development is to use [VirtualBox](http://virtualbox.org/) to run a virtualization image.

Of course check the guides CreateFromScratch and ClasscommInstall.

## SCP File Copy ##
As an alternative to setting up an FTP server on your development sandbox, you could just use SCP like so:
```
scp SourceFile user@host:directory/TargetFile
scp user@host:/directory/SourceFile TargetFile
scp -P 2222 user@host:directory/SourceFile TargetFile
```

## Pre-Populate MySQL ##
As contributing members get Demo Course Content in place, we will release a SQL core file to help pre-populate your deployment with content.

You can get a dump of your own instance by running export in PhpMyAdmin or by running:
```
$ mysqldump <database-name> -u<username> -p >> classcomm.sql
```

You can import this SQL file by running:
```
$  mysql -u<username> -p
mysql> create database cm2;
mysql> use cm2;
mysql> source classcomm.sql
```


## Django Command Extensions ##
Django Command Extensions add commands to manage.py for
[screencast-django-command-extensions](http://ericholscher.com/blog/2008/sep/12/screencast-django-command-extensions/)
Django Command Extensions can be used to take snapshots of the complete project model hierarchy graph.  There are also other features, one that seems useful is some kind of interactive test debugger.


## Profiling Performance ##

### Django ###
[ProfilingDjango](http://code.djangoproject.com/wiki/ProfilingDjango) - Profile Django Views execution time with this profiling script/decorator pattern.  This combined with the already packaged DjangoDebugToolbar will provide insight into the performance of every executable code piece on our server including insight into Database performance at the query level.

### Memory Leaks (Using Django-Dowser) ###
It is very to add on [this app Django-Dowser](http://code.google.com/p/django-dowser/) based on an original CherryPy app called Dowser.  It shows all the Python object counts and allows you to trace them.  Useful tool for tracking down any kind of rare memory problems or to help verify running code.

## Code Review Tools ##

### pylint ###
[pylint](http://www.logilab.org/857) (similar to JSlint) is a Python code review tool.  So far I have not gotten this to run well in this project space, but I will take this up another day.


