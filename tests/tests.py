import os

from django.conf import settings
from django.contrib.auth.models import User
from django.core.urlresolvers import reverse
from django.http import HttpResponse, HttpResponseRedirect
from django.test import TestCase

from tenderize.helpers import tender_hash, tenderize_response, tender_api, tender_multipass
from tenderize.views import login_and_tenderize


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
        self.password = 'password'
        self.tender = 'help.yourapp.com'
        self.expires = 1228117891
        self.secret = 'monkey'
    
    def tearDown(self):
        settings.TEMPLATE_DIRS = self.old_template_dir
    
    def testTenderAPI(self):
        # this is to test if the API is working given the variables you have in settings
        tclient = tender_api()
        self.assertEquals(tclient.raw_data.permalink, settings.TENDER_APP_NAME)
    
    def testTenderHash(self):
        result = tender_hash(self.email, self.expires, self.tender, self.secret)
        self.assertEquals(result, '1937bf7e8dc9f475cc9490933eb36e5f7807398a')
    
    def testTenderizeResponse(self):
        # Tenderized response will contain Tender cookies.
        response = HttpResponse('Test Response')
        response = tenderize_response(response, self.email, {'user': self.user})
        self.assertEqual(response.cookies['tender_email'].value, self.email)
        self.assertEqual(response.cookies['tender_user'].value, self.user)
        self.assertTrue('tender_expires' in response.cookies)
        self.assertTrue('tender_hash' in response.cookies)
    
    def testLoginAndTenderize(self):
        user = User.objects.create_user(self.user, self.email, self.password)
        
        # Correct login returns HttpResponseRedirect
        login = reverse('login_and_tenderize')
        data = {'username': self.user, 'password': self.password}
        response = self.client.post(login, data)
        self.assertTrue(isinstance(response, HttpResponseRedirect))
        self.assertTrue('tender_expires' in response.cookies)
        self.assertTrue('tender_hash' in response.cookies)
        self.assertTrue('tender_email' in response.cookies)
        
        # Bad login returns HttpResponse
        bad_data = {'username': self.user, 'password': 'monkey'}
        response = self.client.post(login, bad_data, follow=False)
        self.assertTrue(isinstance(response, HttpResponse))
        
    def testMultipassToken(self):
        self.assertEquals(tender_multipass('Dmitry Shevchenko', 'dmishe@gmail.com', '2010-01-16T13:19', tender='some_site', sso_secret='some_key'), \
            'mi2sYmBjQXdOt3k7pIS3wWZYTIPnOpLUHwHBHU0eKzsp908zyZ54g3WPOmreGkMddXePgVKncnW5%0A%2B8Cnfbo1gmk%2BTOGCgBkujledRviYwRXK1DppVNwPAGupQLs%2BKYjq%0A')
        
