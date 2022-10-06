from django import template
from django.conf import settings

register = template.Library()

ALLOWABLE_SETTINGS = ('LOGOUT_URL')

# settings value - taken from https://stackoverflow.com/questions/433162/can-i-access-constants-in-settings-py-from-templates-in-django
@register.simple_tag
def settings_value(name):
    if name in ALLOWABLE_SETTINGS:
        return getattr(settings, name, '')
    return ''