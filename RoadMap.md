# Classcomm Road-Map #

## The Move to HTML5 ##
Presently Django and contributing apps generally output code that validates doctype as XHTML which has been the de facto standard since folks migrated away from HTML4.  With the advent of HTML5 coming to light, and all the awesome features it brings to the table (example: native HTML support for videos) and WebGL it is no doubt that clascomm will be adopting html5 in the future--**committing to aspects of HTML5 in trunk by middle of 2012** (video support seems like something we'd feel confident supporting by then).

Personally I have been learning about this topic from the book <a href=''>Introducing HTML 5</a> and it is a top reading pick for the close of 2010.  Unfortunately web standards fall subjects to browser support, and as typical, Microsoft IE makes html5 support a lower priority as does browser upgrade timeliness in general.


## New Feature Development ##
The coming year is about introducing new Django versions to improve our project, taking advantage of tests best practice, as well as continuing third party exploration and new feature development. The following items are keynotes:

### Adding/Fixing Tests; Documenting best practices ###
With the release of Django 1.3 coming in February of 2011 we will be adding and maintaining unitest2 code for each of our applications in classcomm.  This along with continuing to document and improve our best practices will lead to increased user and developer confidence.

### Classcomm Quizes ###
Classcomm needs to meet all the buissness requirements of Mallard Quizes and to do this will include a quizzes app in classcomm.  First mature version of this expected the beginning of the second half of 2011.

### Classcomm Videos/Lectures ###
As mentioned under HTML5, we will most likely employ HTML5 standards and best practices to deliver videos and improve media delivery within classcomm overtime.  Expected the end of 2011 or so.

### Web 2.0 Default Styling Selector and improved Graphic Design ###
We aim to package 3-6 default styling packages for at least core parts of the app, and to allow configuring these dynamically in the admin by 2012.

### Logging and enabling Sentry Dashboard ###
We will be adding logging/improving sessions handling and packaging Sentry with classcomm.  With the advances that HTML5 brings we will also consider again using the Django Messages Framework for delivering application error messages to the User.

### Localization Efforts ###
We are looking to implement Django localization in hardened parts of the project.  Any language is a possibly, but we are definitely doing English, German, Spanish, Italian and Chinese.  Probably will begin to see a couple of this included late 2011.