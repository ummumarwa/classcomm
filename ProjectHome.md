## Current Version ##
0.6.0 running with Django 1.3.1 stable

## Development Status ##
7/4/2012 - In the process of converting project over to gitt.  Want to be more community driven development.

## Description: ##
Perfect for companies, colleges, schools, community organizations and collectives wishing to deliver courses via the Internet on an internal deployment of Classcomm.  Classcomm is a set of tools for instructors and students to hand-in assignments, communicate effectively on the web, and learn new materials.

## Live Demo ##
Presently the best way to experience Classcomm is with our advertisement-free Live Demo.  You can register your free account with database encrypted password, and try out the student and instructor views.  Soon you will additionally be able to create Courses on our Demo system for Demo purposes, but possibly also to offer up for open enrollments and trial your own course materials.

Please try our Live Classcomm Demo on http://classcomm.net/ <br />
Register your account and complete the activation e-mail to gain access to a deployed instance of Classcomm.  Then enroll in any of our free Demo courses set for open\_enrollment to demo the student portal and instructor portal.  I'll be adding create-a-course app soon and better hooks so you'll be able to Demo the site-wide side better.

## Current Features: ##
  * Enroll in Courses and accept Assignments electronically.
  * Serve all your media behind time-generated protected URLs.
  * Provide students with internal and external course information and resources.
  * Deploy quickly and rest sound on the more proven security of the Django framework.
  * Supports asynchronous Course enrollment timetables, open enrollments and roster tools.
  * Customized Django admin provides administrators with application data management tools.
  * Project uses Hardened Web Technologies.
  * Choose your own Database Implementation and use any of the libraries available with the Django Object Relational Mapper.
  * Integrate our internal Django User model with your network authentication such as LDAP or OpenID using custom Django Authentication Back-ends.  These back-ends are chainable to support multiple authentication systems, and can be made to work with the User model that is available across apps in the Django-classcomm project.




## System Requirements ##
Any 2Ghz+ CPU, 2GB+ memory, 50GB +Hard Disk system or better running Ubuntu Linux.<br />
**Better Systems can support more Users, more content and more services.**

### Live Demo Currently Running On ###
  * Django 1.3
  * Python 2.6
  * Apache 2.x with mod\_auth\_token 1.0.6 configured.
  * MySQL 5 Database (using MyISAM tables to enable searching in admin tool)
> > Other database support inherent in Django [MySQL, Postgresql, Oracle, and several other adapters have been written].


### Client ###
Any fairly modern to stale web-browser with an Internet connection should get valid app pages served for the URL to deployed application instance.  Sessions Requires Cookies, and this project uses cookies!  New versions and future versions of classcomm ship with AJAXian features so your browser should be able to support that.


## Technologies ##
[Python](http://www.python.org),
[Django Framework](http://www.djangoproject.com),
[Apache](http://www.apache.org),
[SQL database](http://www.mysql.org).


## History and Statistics ##

I started this Django project began the very end of 2007 as part of my J.Scholar Honors at <a href='http://illinois.edu/'>Illinois</a>.  Inspired by the simple design of Course CMS prototype with the same name written in PHP, and used by the [UIUC NetMath Program](http://netmath.math.uiuc.edu/).  The goal of this open-source Django project <i>Classcomm</i> has been to develop a web application CMS inside a web framework that could make quality guarantees while facilitating add-on development and agile feature releases for such a product while keeping pace with the latest web standards.  The flexibility, stability and security specifications of the latest Django releases has made this an up-and coming technology suite for delivering Courses on the Web that schools will be able to deploy to their own servers or purchase instances through cloud providers for offering these services.  We hope to offer and support such services ourselves in the future.



