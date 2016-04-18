# Introduction #

A Django Classcomm project is a dynamic website application ready for deployment for your target audience.  The primary points of configuration are the **settings.py** file, and the Django Admin.  There are several points of configuration that will need to be set by an a knowledgeable systems administrator for any Classcomm install.


# Settings.py File #

Find and configure the following Items in the settings.py file:

The **Secret Key** is a key used in the generation of unique session ids for Users.  This should be set to a unique value and kept private from Users as it will be used only by the seb server.
```
# Make this unique, and don't share it with anybody.
# Run generate_key.py in the classcomm directory to generate a random key value.
SECRET_KEY = 'r$rh(0u8n&li68^v)eijdi-gvtsk6yqpx#q06j0&gboa1innbu'
```