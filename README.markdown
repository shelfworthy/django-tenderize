Info
====

Tender uses tasty cookies to log your users in.
http://help.tenderapp.com/faqs/setup-installation/login-from-cookies

This app includes a view like `django.contrib.auth.views.login` that in addition to logging a user in as normal, sets the cookies required by Tender. Yum.

Please direct all bugs and feature requests to the lighthouse page for this project:

http://chrisdrackett.lighthouseapp.com/projects/37333-python-tender/overview

Requirements
============

To use the API parts of tender you will need to install the following on your python path:

* [tpg](http://christophe.delord.free.fr/tpg/index.html)

Installation
============

1. Checkout the project into a folder called `tenderize` on your python path:

	git clone git://github.com/chrisdrackett/django-tenderize.git tenderize

2. Update the submodules (this gets the python tender API wrapper)

	cd django-tenderize/

	git submodule update --init

2) Add `tenderize` to your installed apps, and add the following to `settings.py`:

TENDER_APP_NAME = 'appname' # your tender app name, <appname>.tenderapp.com/
TENDER_EMAIL = 'email@address.com' # this is the default email that will be used for API requests
TENDER_PASSWORD = 'xxxx' # the password that goes along with the above email
TENDER_COOKIE_DOMAIN = '.mysite.com'
TENDER_SECRET = "???" # get from tender
TENDER_DOMAIN = 'support.mysite.com' # your.tenderapp.com
TENDER_COOKIE_AGE = 1209600 # how long the cookies will last (2 weeks in seconds)

3) Add the following to urlpatterns in `urls.py`:

url(r'^login/$', 'tenderize.views.login_and_tenderize', name="login")

4) Run syncdb

Tender API
============

Documentation of the tender API is coming as the python wrapper matures.
You can initiate the api using the helper function 'tender_api' in helpers.py.
This function will default to using the email and password you have in settings,
but can be overridden.

Currently there is a helper in place to sync categories from tender into your database.
This should help you display categories without hitting tender. We also have a shortcut
to create discussions directly from the django Category object.