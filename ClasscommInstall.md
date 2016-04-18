# Introduction #

This document describes steps for configuring classcomm on Ubuntu Server 10.10 64-bit. Perhaps first you should create a VirtualBox machine running Ubuntu following our instructions in the CreateFromScratch document, or you already have running your own Ubuntu Linux server.  Either way, these instructions will help you deploy classcomm to your server.

**Estimated Total Time: 1.5 hours**<br />


## Install Necessary Packages ##
**Estimated Time: 30 minutes**

Now we want to load up our system with all of the tools we need to run classcomm.  Run the following commands:
```
sudo apt-get install build-essential
sudo apt-get install apache2
sudo apt-get install apache2-threaded-dev
sudo apt-get install libapache2-mod-wsgi
sudo apt-get install sysvinit-utils
sudo apt-get install python-mysqldb
sudo apt-get install python-dateutil
sudo apt-get install python-docutils
sudo apt-get install python-feedparser
sudo apt-get install subversion
sudo apt-get install automake
sudo apt-get install linux-headers-$(uname -r)
```

Now install the MySQL server and choose a password for the root user.
```
sudo apt-get install mysql-server
```

Now install and configure NTPD (Network Time Protocol Daemon)
```
sudo apt-get install ntp
```
See Also [Synchronization using NTP](https://help.ubuntu.com/community/UbuntuTime#Time)


## Test Apache ##
**Estimated Time: 5 minutes**

Now we should have a running apache server.  Determine your 192.168.56.X IP address:
```
ifconfig | less
```
Now try connecting to that address in a web browser.  You should see an "It Works!" page.


## Checkout & Install Django ##
**Estimated Time: 10 minutes**

Now we want to grab and insall the latest Django release to work with classcomm.
**Latest Classcomm-Django Version: 1.2.3**
```
cd ~
wget -O Django-1.2.3.tar.gz http://www.djangoproject.com/download/1.2.3/tarball/
tar xzvf Django-1.2.3.tar.gz
cd Django-1.2.3
sudo python setup.py install
```


## Checkout Classcomm ##
**Estimated Time: 10 minutes**

Now we want to check out our classcomm project to our guest host.
```
sudo rm -rf /var/www
sudo svn checkout http://classcomm.googlecode.com/svn/trunk/ /var
```


## Install mod\_auth\_token ##
**Estimated Time: 10 minutes**

We use Apache module mod\_auth\_token to secure protect our media files from unauthorized users.  We need to download and configure this module for Apache on our classcomm host:

```
cd ~
wget "http://mod-auth-token.googlecode.com/files/mod_auth_token-1.0.5.tar.gz"
tar xvzf mod_auth_token-1.0.5.tar.gz
cd mod_auth_token-1.0.5/
sudo rm missing
sudo ln -s /usr/share/automake-1.11/missing missing
sudo rm config.guess
sudo ln -s /usr/share/automake-1.11/config.guess config.guess
sudo rm config.sub
sudo ln -s /usr/share/automake-1.11/config.sub config.sub
sudo rm COPYING
sudo ln -s /usr/share/automake-1.11/COPYING COPYING
sudo rm install-sh
sudo ln -s /usr/share/automake-1.11/install-sh install-sh
sudo ./configure
sudo make
sudo make check
sudo make install
sudo service apache2 restart
```


## Create Default Database ##
**Estimated Time: 5 minutes**

Now we will create our MySQL database and user with permissions:
```
# Use your root SQL user password from during the install
mysql -u root -p
mysql> create database cm2;
# Change Sammy2son to be an appropriate user password and remember it--you will need to update it to your settings.py file later.
mysql> grant all privileges on cm2.* to cm2@localhost identified by 'Sammy2son';
mysql> quit
```


**Note:** If you are setting up a development instance or are interested in running the complete project test suite (end-users can skip this) then you will need to also grant more permissions using your run\_as user and the chosen password.
```
mysql> grant all privileges on test_cm2.* to cm2@localhost identified by 'Sammy2son';
Query OK, 0 rows affected (0.00 sec)

mysql> grant drop on test_cm2.* to cm2@localhost identified by 'Sammy2son';
Query OK, 0 rows affected (0.00 sec)

mysql> grant delete on test_cm2.* to cm2@localhost identified by 'Sammy2son';
Query OK, 0 rows affected (0.00 sec)

mysql> grant create on test_cm2.* to cm2@localhost identified by 'Sammy2son';
Query OK, 0 rows affected (0.00 sec)
```


## Configure Classcomm ##
**Estimated Time: 10 minutes**

Copy default Apache config file to your local Apache install.  Our default file configures mod\_auth\_token, serving media files and points Apache at a default classcomm.wsgi file for serving the Django app.
```
sudo cp /var/apache-config/httpd.conf /etc/apache2/.
sudo service apache2 restart
```

Now set some permissions:
```
# Apache run as use is www-data
sudo chown -R www-data /var/www
```

Now populate the database with initial tables:
```
# Correct the database user/password in settings.py file:
# nano is a text editor ctrl+s to save and ctrl+x to exit
sudo nano /var/django_projects/classcomm/settings.py

# Now run the following command to create the initial database tables and superuser:
python /var/django_projects/classcomm/manage.py syncdb
# Be sure to create a new superuser--this is your first classcomm account!
```


## Secure Your Instance ##
**Estimated Time: 10 minutes**

Congratulations, you are now running an instance of freely available open source software.  You should already have changed your database settings away from the default password of 'Sammy2Son'.  Now you will also want to:
  1. Secure mod\_auth\_token passwords
  1. Change SECRET\_KEY setting

```
# nano is a text editor ctrl+s to save and ctrl+x to exit
# Look for line AuthTokenSecret and adjust to new secret pass in file:
sudo nano /etc/apache2/httpd.conf
# Look for line AUTH_TOKEN_PASS and adjust to SAME secret pass as previous file:
sudo nano /var/django_projects/classcomm/settings.py
# Now in the same file look for SECRET_KEY setting and change this to a different key of similar length.  In case you closed the file that is:
sudo nano /var/django_projects/classcomm/settings.py
```

## Connecting to Classcomm ##
**Estimated Time: 5 minutes**

Once we have verified our web server is online, we can begin using classcomm.
The app home is: http://192.168.56.*X*/student/
This can be administered at: http://192.168.56.*X*/classcomm/admin/

You created a classcomm use when you ran the python manage.py syncdb command earlier to create the database tables.

## Set Sites Data for deployed instance ##

Our project uses the **django.contrib.sites** package. It is a hook for associating objects and functionality to particular Web sites, and it’s a holding place for the domain names and “verbose” names of your Django-powered sites.

For Example, my virtual machine is configured with:
```
'Domain Name:' 192.168.56.101 and 'Display Name:' Classcomm 
```

## Create Default Auth.Groups ##
**Estimated Time: 5-10 minutes**

Now efore we can take full advantage of our new Django-Classcomm environment we want to create the Default Groups with set default permissions using the Django-Classcomm admin.  These permissions apply across Courses and care should be taken to not extend your User roles past where they should be.  Individual Users may be granted additional permission on a per User basis however, we imagine this will not typically be necessary.

Our models.py Models now automatically assign/remove Users from these Default Admin Groups, and otherwise staff users have no permissions by default.  The Group Automation code operates under the assumption that the corresponding bindings are created.  Now Create each Group with the exact name and the recommended permissions (permissions assigned will be the actual ones you define--Users get them by being assigned as acting Course Director, Instructor, Mentor or Mentor Assign so be sensible and use our recommended defaults.

### Course Director ###
```
# Add New Director Group
Name: Director
Recommended Permissions*:
student_portal->announcement(add, change, delete)
student_portal->assignment(add, change, delete)
student_portal->due_date_override(add, change, delete)
student_portal->information(add, change, delete)
student_portal->resources(add, change, delete)
student_portal->instructor(add, change, delete)
student_portal->mentor(add, change, delete)
# Optionally:
student_portal->submissions(add, change, delete)
student_portal->enrollment(add, change, delete)
```

**Note on Submissions:** Perhaps you want to exclude Submissions as a safety net to guarantee that a student Submission is not tampered with.  Well trust your users, and look to the logs to find information about Deleted Submissions.  It is true that a User's Submissions could vanish if the Enrollment is changed to a different User in the admin, but that would be a lack of trust on the active Directors part, and also our validation could pick this up as a duplicate.

**Note on Enrollments:** Having a Course Director is a good spot to handle Enrollments and Registrations, but it may suit you also to write your own connector script to automate Enrollment creation or simply register all of your courses for the OPEN\_ENROLLMENTS feature.


### Instructor ###
```
# Add New Instructor Group
Name: Instructor
Recommended Permissions*:
student_portal->announcement(add, change, delete)
student_portal->assignment(add, change, delete)
student_portal->due_date_override(add, change, delete)
student_portal->grade(add, change, delete)
student_portal->information(add, change, delete)
student_portal->resources(add, change, delete)
# Optionally:
student_portal->mentor(add, change, delete)
```

**Note:** We omit Submissions to prevent an Instructor or Mentor from clearing a student Submission on accident for instance.  We leave this permission for students using the student\_portal Assignment handin tool, and optionally for Course Directors to oversee special circumstance-related Homework Submissions using the admin tool.

### Mentor ###
```
# Add New Mentor Group
Name: Mentor
Recommended Permissions*:
student_portal->announcement(add, change, delete)
student_portal->due_date_override(add, change, delete)
student_portal->grade(add, change, delete)
# Optionally:
student_portal->due_date_override(add, change, delete)
# Optional, but probably not typical since this would effect all Mentors and Courses:
student_portal->information(add, change)
student_portal->resources(add, change)
```