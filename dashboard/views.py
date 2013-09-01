from global_decorators import render_to
from django.template import Context, loader
from admin.settings import get_setting
from django.http import HttpResponseServerError
from announcements.models import Announcement
import sys


@render_to('dashboard.html')
def index(request):
    message = get_setting('welcome_msg')
    title = "Dashboard"
    icon = "home"
    announcements = Announcement.latest(3)
    return locals()


def custom_500(request):
    t = loader.get_template('500.html')
    value, tb = sys.exc_info()[:2]
    return HttpResponseServerError(t.render(Context({
        'exception_value': value,
        'traceback': tb
        })))