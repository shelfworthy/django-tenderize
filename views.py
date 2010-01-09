from django.http import HttpResponseRedirect
from django.conf import settings

from helpers import multipass_url

def multipass_login(request):
    ''' Helper view for tenderapp.com authentication'''
    if request.user.is_authenticated():
        return HttpResponseRedirect(multipass_url(
            settings.TENDER_DOMAIN,
            request.user,
        ))
    else:
        return HttpResponseRedirect(reverse('login') + '?next=' + reverse('multipass'))