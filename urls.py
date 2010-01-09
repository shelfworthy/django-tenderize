from django.conf.urls.defaults import *

urlpatterns = patterns('tenderize.views',
    url(r'^tender_multipass/$', 'multipass_login', name='multipass'),
)


