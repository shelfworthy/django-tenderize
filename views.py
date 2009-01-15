from django.http import HttpResponseRedirect
from django.contrib.auth.views import login
from django.contrib.auth import REDIRECT_FIELD_NAME
from django.contrib.auth.forms import AuthenticationForm
from django.views.decorators.cache import never_cache

from helpers import tenderize_response

def login_and_tenderize(request, template_name='registration/login.html', redirect_field_name=REDIRECT_FIELD_NAME):
    "Displays the login form and handles the login action. Sets Tender cookies if successful."
    response = login(request, template_name, redirect_field_name)    
    # login returns a HttpResponseRedirect if successful.
    if isinstance(response, HttpResponseRedirect):
        # Get email from the logged in user.
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            if request.session.test_cookie_worked():
                request.session.delete_test_cookie() 
            # Tender in here
            response = HttpResponseRedirect(redirect_to)
            response = tenderize_response(response, user)
            return response
    else:
        form = AuthenticationForm(request)
    request.session.set_test_cookie()
    if Site._meta.installed:
        current_site = Site.objects.get_current()
    else:
        current_site = RequestSite(request)
    return render_to_response(template_name, {
        'form': form,
        redirect_field_name: redirect_to,
        'site_name': current_site.name,
    }, context_instance=RequestContext(request))
login_and_tenderize = never_cache(login_and_tenderize)
