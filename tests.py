import os

from django.conf import settings
from django.contrib.auth.models import User
from django.core.urlresolvers import reverse
from django.http import HttpResponse, HttpResponseRedirect
from django.test import TestCase

from tenderize.helpers import tender_api

class TenderizeTest(TestCase):
    urls = 'tenderize.tests.test_urls'
    template_dirs = [
        os.path.join(os.path.dirname(__file__), 'templates'),
    ]
    
    def setUp(self):
        # Template nessecary to test login.
        self.old_template_dir = settings.TEMPLATE_DIRS
        settings.TEMPLATE_DIRS = self.template_dirs
        
        self.user = 'user'
        self.email = 'user@gmail.com'
        self.tender = 'help.yourapp.com'
        self.expires = 1228117891
        self.secret = 'monkey'
    
    def tearDown(self):
        settings.TEMPLATE_DIRS = self.old_template_dir
    
    def testTenderAPI(self):
        # this is to test if the API is working given the variables you have in settings
        tclient = tender_api()
        self.assertEquals(tclient.raw_data.permalink, settings.TENDER_APP_NAME)
    
    def testMultipassToken(self):
        tclient = tender_api()
        
        multipass(expires=None, username=None, email=None, unique_id=None, trusted=True, avatar_url=None, extras=None):
        
        self.assertEquals(tclient.multipass(username='Dmitry Shevchenko', email='dmishe@gmail.com', expires='2010-01-16T13:19'), \
            'mi2sYmBjQXdOt3k7pIS3wWZYTIPnOpLUHwHBHU0eKzsp908zyZ54g3WPOmreGkMddXePgVKncnW5%0A%2B8Cnfbo1gmk%2BTOGCgBkujledRviYwRXK1DppVNwPAGupQLs%2BKYjq%0A')
