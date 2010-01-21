import hmac
from time import time
from datetime import datetime, timedelta

from django.conf import settings
from django.utils.http import cookie_date
from django.utils.hashcompat import sha_constructor

from tenderize.pytender import TenderClient
from tenderize.models import Category

# helper to setup an instance of the API

def tender_api():
    return TenderClient(
        app_name    = settings.TENDER_APP_NAME,
        user_email  = settings.TENDER_EMAIL,
        secret      = settings.TENDER_SECRET
    )

def multipass_url(url, user, display_name=None, **kw):
    if user.is_authenticated():
        return tender_api().multipass_url(url, tender_api().multipass(
            username=display_name or user.username,
            email=user.email,
            unique_id=str(user.id),
            **kw
        ))
    else:
        return url

def sync_categories(email=None):
    api = tender_api()
    
    Category.objects.all().delete()
    
    for tender_cat in api.categories():
        Category.objects.create(
            id=tender_cat.id,
            name=tender_cat.name,
            permalink=tender_cat.permalink,
            url=tender_cat.href
        )
