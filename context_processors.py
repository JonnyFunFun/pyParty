from django.conf import settings
from admin.settings import get_setting

def template_debug(context):
    return {'TEMPLATE_DEBUG': settings.TEMPLATE_DEBUG}

def settings_for_view(context):
    return {'SITE_NAME': get_setting('site_name'),
            'SITE_TITLE': get_setting('site_title'),
            'ENABLE_MUSIC': get_setting('enable_music'),
            'ENABLE_BENCHMARKS': get_setting('enable_benchmarks'),
            'ENABLE_GALLERY': get_setting('enable_gallery'),
            'ENABLE_TOURNAMENTS': get_setting('enable_tournaments'),
            'ENABLE_SERVERS': get_setting('enable_servers'),
            'ENABLE_NOMS': get_setting('enable_noms')
    }

def active_section(context):
    try:
        active = context.path.split("/")[1]
    except:
        active = ''
    return {'ACTIVE_SECTION': active}