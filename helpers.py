import hmac
from time import time

from django.conf import settings
from django.utils.http import cookie_date
from django.utils.hashcompat import sha_constructor

from tenderize.pytender import TenderClient
from tenderize.models import Category

# helper to setup an instance of the API
def tender_api(email=None, password=None):
    return TenderClient(
        app_name=settings.TENDER_APP_NAME,
        user=email or settings.TENDER_EMAIL,
        password=password or settings.TENDER_PASSWORD
    )

def sync_categories(email=None, password=None):
    api = tender_api(email, password)
    
    Category.objects.all().delete()
    
    for tender_cat in api.categories():
        category, created = Category.objects.get_or_create(
            id=tender_cat.id,
            defaults={
                'name':tender_cat.name,
                'permalink':tender_cat.permalink
            }
        )
        
        if not created:
            category.name=tender_cat.name
            category.permalink=tender_cat.permalink
            category.save()

# help.yourapp.com/user@gmail.com/1228117891
HASH_FORMAT = "%s/%s/%s"
# tender_xxx
COOKIE_FORMAT = "tender_%s"
# support.tender.com
TENDER_DOMAIN = settings.TENDER_DOMAIN
# .tender.com
COOKIE_DOMAIN = TENDER_DOMAIN[TENDER_DOMAIN.find('.'):]
# get from Tender - http://support.example.com/settings
SECRET = settings.TENDER_SECRET
# cookie age in seconds
AGE = settings.TENDER_COOKIE_AGE

def tender_hash(email, expires, tender=TENDER_DOMAIN, secret=SECRET):
    """
    Calculates and returns a tender_hash.
    
    """
    s = HASH_FORMAT % (tender, email, expires)
    sig = hmac.new(secret, digestmod=sha_constructor)
    sig.update(s)
    return sig.hexdigest()
    
def tenderize_response(response, email, extra_cookies=None):
    """
    Adds tender cookies to a HttpResponse.
    
    """
    expires = time() + AGE
    # Tender wants expires in epoch seconds, expires is set with `cookie_date`
    tender_expires = int(expires)
    cookie_expires = cookie_date(expires)
    hashed = tender_hash(email, tender_expires)
    cookies = dict(expires=tender_expires, hash=hashed, email=email)
    # Add extra Tender cookies: http://tinyurl.com/8vwxyw
    if extra_cookies is not None:
        cookies.update(extra_cookies)
    for key, value in cookies.iteritems():
        cookie = COOKIE_FORMAT % key
        response.set_cookie(cookie, value, expires=cookie_expires, domain=COOKIE_DOMAIN)
    # response.set_cookie() incorrectly adds quotes to the tender_email cookie.
    # To remove the quotes we set the value again.
    response.cookies['tender_email'].coded_value = email
    return response
    
def detenderize_response(response, extra_cookie_keys=None):
    """
    Removes Tender cookies from a HttpResponse.
    
    """
    # Things getting a bit less dry - probably want to toss these
    # cookie keys out somewhere
    cookie_keys = ["expires", "hash", "email"]
    
    for cookie_key in cookie_keys:
        cookie = COOKIE_FORMAT % cookie_key
        response.delete_cookie(cookie, domain=COOKIE_DOMAIN)

    return response
