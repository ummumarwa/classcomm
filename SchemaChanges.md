# Introduction #

We've recently adopted a third-party OSS technology Django-South for handling Database Schema migrations in classcomm.  It


# Details #

Default Django usage has the manage.py syncdb command which will create new models, but cannot change the schema of existing models as they change which therefore locks down the database and restricts development or requires manual SQL schema changes or using a tool such as PHPMyAdmin.  Instead now we can automate these schema changes and keep a history log for database changes going forward using Django-South.  This tool (which disables normal syncdb in favour of its specialized command set) is able to auto-generate schema altering Python code which South then uses to actually modify the existing database tables.

## Initial Configuration ##
Since our app is already created, we have South create the initial migration and fake apply it
```
python manage.py convert_to_south student_portal
```


## Basic Usage ##
We can list the current migrations and see which ones have been applied by running:
```
sudo python manage.py migrate --list

# Sample Output:
 student_portal
  (*) 0001_initial
  (*) 0002_rename_enrollment_length
  (*) 0003_add_grade_date
  (*) 0004_auto_add_extra_credit

 indexer
  (*) 0001_initial

 overseer
  (*) 0001_initial
  (*) 0002_auto__add_subscription__add_unverifiedsubscription

 output_validator
  (*) 0001_initial

```


## Auto-Generate schema change code when adding a new Model ##
```
$ sudo python manage.py schemamigration student_portal --add-model ExtraCredit
$ sudo python manage.py migrate student_portal
```
The first line generates the new schema migration file.  The second trys to apply the migration.  It is possible to use this tool to generate data migrations of existing tables as well--please see the [South documentation](http://south.aeracode.org/docs/tutorial/part3.html) for details as in the past these have been written by hand we choose to continue to do so in our releases.