from django.conf import settings
from admin.settings import get_setting
from music.models import Music


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
            'ENABLE_NOMS': get_setting('enable_noms'),
            'THUMB_X': settings.THUMBNAIL_SIZE[0],
            'THUMB_Y': settings.THUMBNAIL_SIZE[1],
            'MUSIC_PLAYING': Music.currently_playing()
    }


def active_section(context):
    try:
        active = context.path.split("/")[1]
    except:
        # shouldn't ever fail here
        active = ''
    return {'ACTIVE_SECTION': active}