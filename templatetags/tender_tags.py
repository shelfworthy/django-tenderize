from django import template
from django.conf import settings

from tenderize.helpers import multipass_url

register = template.Library()

@register.simple_tag
def tender_url(user, display_name=None, avatar_url=None, extras=None):
    return multipass_url(settings.TENDER_DOMAIN, user, display_name, avatar_url, extras)
    