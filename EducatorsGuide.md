# Introduction #

This page describes using screen shots the tools available to administer courses using classcomm.  This document contains screenshots organized by different sections of the Classcomm Project:
  * [EducatorsGuide#Django\_Admin](EducatorsGuide#Django_Admin.md)
  * [EducatorsGuide#Student\_Pages](EducatorsGuide#Student_Pages.md)
  * [EducatorsGuide#Instructor\_Pages](EducatorsGuide#Instructor_Pages.md)
  * [EducatorsGuide#Debug\_Toolbar](EducatorsGuide#Debug_Toolbar.md)

# Django Admin #
The Admin comes bundled with the Django framework--it provides the systems administrators access as well permissions hooks for adding other authorized Users.  The admin allows searching, listing, and in some cases creating/modifying data in your Classcomm deployment.

## Admin Login ##
Login page for the project Admin interface.
<br />
![http://classcomm.googlecode.com/files/adminlogin.jpg](http://classcomm.googlecode.com/files/adminlogin.jpg)
<br />

## Main Page ##
Here you can see all the types of objects the system uses.  From here we can browse what is in the system already and add/delete content.  **Current version may have modified datatypes.**
<br />
![http://classcomm.googlecode.com/files/adminmain.jpg](http://classcomm.googlecode.com/files/adminmain.jpg)
<br />

## Add Course ##
From the main page, click add by Course and get this view:
<br />
![http://classcomm.googlecode.com/files/addcourse.jpg](http://classcomm.googlecode.com/files/addcourse.jpg)
<br />

## Add Course Assignment ##
View for adding an Assignment.
<br />
![http://classcomm.googlecode.com/files/addassignment.jpg](http://classcomm.googlecode.com/files/addassignment.jpg)
<br />

## Add Course Enrollment ##
This enrolls the classcomm user in the newly created Math 415 course starting today and ending 12 weeks from now.  The user does not have a mentor and will not be able to login after the course end date.
<br />
![http://classcomm.googlecode.com/files/addenrollment.jpg](http://classcomm.googlecode.com/files/addenrollment.jpg)
<br />


# Student Pages #

## Login ##
The default login view.  **Outdated, this image needs to be updated**
<br />
![http://classcomm.googlecode.com/files/studentlogin.jpg](http://classcomm.googlecode.com/files/studentlogin.jpg)
<br />

## Home ##
Lists all current course enrollments.
<br />
![http://classcomm.googlecode.com/files/studenthome.jpg](http://classcomm.googlecode.com/files/studenthome.jpg)
<br />

## Course Home ##
Clicking on the course name will load the course home and expanded course specific menus.
<br />
![http://classcomm.googlecode.com/files/coursehome.jpg](http://classcomm.googlecode.com/files/coursehome.jpg)
<br />

## Course Assignments ##
The Course Assignments page lists all course assignments, secure downloads for provided files, and the ability to securely upload completed work (if enabled for assignment).
<br />
![http://classcomm.googlecode.com/files/courseassignments.jpg](http://classcomm.googlecode.com/files/courseassignments.jpg)
<br />


# Instructor Pages #
The Instructor portal is a new addition that fullfills the granular needs of roles created by our logical creation of Course Directors, Instructors and Mentors.
## Student Grade Report View ##
This view in the Instructor portal opens up Grading functionality to Instructors/Mentors
<br />
![http://classcomm.googlecode.com/files/GradeReport.png](http://classcomm.googlecode.com/files/GradeReport.png)
<br />


# Debug Toolbar #
Classcomm Django is now packaged with the Django Debug Toolbar which takes Debug mode to a new level of detail.  This feature is great for administrators wishing to explore site performance, and most excellent for Classcomm Developers in helping optimize their code and detect bugs before they end up in a release.
## Collapsed Debug Toolbar View ##
The Debug Toolbar is enabled only for the IPs specified in [SettingsDotPy](SettingsDotPy.md) under INTERNAL\_IPS setting.  When an enabled user accesses the site it appears at a tab on the right side of the view.
<br />
![http://classcomm.googlecode.com/files/DebugToolbarCollapsed.png](http://classcomm.googlecode.com/files/DebugToolbarCollapsed.png)
<br />

## Expanded Debug Toolbar Side View ##
Clicking on the Debug Toolbar tab reveals basic stats about the current page view and links to full pages of information.
<br />
![http://classcomm.googlecode.com/files/DebugToolbarSideShow.png](http://classcomm.googlecode.com/files/DebugToolbarSideShow.png)
<br />

## Expanded Debug Toolbar SQL View ##
Clicking on the SQL section expands out to a view which shows the order of SQL queries, what they were, and the time it took each one to execute.
<br />
![http://classcomm.googlecode.com/files/DebugToolbarSQLShow.png](http://classcomm.googlecode.com/files/DebugToolbarSQLShow.png)
<br />