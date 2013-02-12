from django.conf import settings
from admin.settings import get_setting

def template_debug(context):
    return {'TEMPLATE_DEBUG': settings.TEMPLATE_DEBUG}

def site_name(context):
    return {'SITE_NAME': get_setting('site_name')}

def site_title(context):
    return {'SITE_TITLE': get_setting('site_title')}