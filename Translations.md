# Introduction #

Initial Django-Classcomm prototype was entirely one Djagno app-space named handin.  That app is now called student\_portal and also supports the core logical data models.  It so happens that student\_portal is our initial target app for translation.  Since our project integrates with Django-Registration which maintains its package translations, and the Django web framework maintains translations as well as providing tools for carrying out the translations our tasks are therefore simplified and manageable.

Please consider applying your language expertise to start new language translations or improve existing ones for this open source project.  Remember that English is the source language so knowledge of English will be important to translate to your target language.

**5/18/2011** -- Currently I am in the process of converting the templates, models and related static text of the student\_portal app to support language translations in the experimental SVN classcomm branch.


# Details #

## Hosting and Translation Project ##

Main code hosting is here on Google Code, however we are electing to create and maintain a [transifex project](https://www.transifex.net/projects/p/classcomm/) for hosting translations, but mainly for facilitating the translation process among the different language teams. At any time the current set of resources can be exported from the **transifex poject** and imported into classcomm-dev and eventually updated in Google Code and mirrored repository sites.

For each candadite language I Will:

  1. Generate the new language files for target language and check it in to source control.
  1. Load the newly generated file in preferred translation suite Django-Rosetta and take on all of the suggestions and check in this updated file.
  1. Add the resource file to the [transifex project](https://www.transifex.net/projects/p/classcomm/) where it can be improved and refined by the contributing language experts.

Finally whenever we hit development releases I can pull the latest translations from the transifex project, and when new features are added or translations strings change I can bounce that back into the transifex project for further improvement.

## Django-Rosetta ##

[Django Rosetta](http://code.google.com/p/django-rosetta/) is a pluggable app that can be added to any Django project space and it will allow the system admin (is\_super\_user) or anyone listed in the translations group to view the complete set of locale language files in the project space.

This is not all, this app shows tallys, fuzzy flag, originals, occurances and allows real-time editing of the translation files.  And this is not all, Django-Rosetta will even query the [Google AJAX Language API](http://code.google.com/apis/ajaxlanguage/) and populate any field with the given suggestion translation!  For Italian, these translations appear by default more accurate and precise than what [Babel Fish](http://babelfish.yahoo.com/) could come up with, or even my own brain!

Best of all, this can take editing the translations away from the editor and into the browser where modern spell checkers can more easily be applied.  Using a browser like the latest FireFox allows several different language dictionaries to be downloaded and installed into the browser which further helps guarantee accuracy and quality in translation.  Using FireFox with your target dictionary installed is the preferred method of translating strings on the transifex project pages from the initial files generated with the aide of Django-Rosetta.


# Web Resources on Django Translations #

I would consider these resources less relevant for anyone wishing to simply contribute translations, but for the technically savvy or for those looking for more answers and information, look no further:

0 Official Docs: [The Primer](http://docs.djangoproject.com/en/dev/topics/i18n/),  [localization](http://docs.djangoproject.com/en/dev/topics/i18n/localization/),  [internationalization](http://docs.djangoproject.com/en/dev/topics/i18n/internationalization/),  [using internationalization](http://docs.djangoproject.com/en/dev/howto/i18n/) and [deploying translations](http://docs.djangoproject.com/en/dev/topics/i18n/deployment/).

1 [Django Advent i18n-l10n-improvements](http://djangoadvent.com/1.2/i18n-l10n-improvements/).

2 [blog post on setting up project for internation support](http://devdoodles.wordpress.com/2009/02/14/multi-language-support-in-a-django-project/)

3 [Video Lecture on Transifex](http://python.mirocommunity.org/video/1210/painless-django-app-localizati)