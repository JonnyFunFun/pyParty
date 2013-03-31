from decorators import admin_only
from global_decorators import render_to
from django.contrib.auth.models import User
from django.views.decorators.http import require_POST
from django.http import HttpResponseRedirect, HttpResponse
from django.contrib import messages
from settings import save_setting, get_setting
from models import PYPARTY_SETTINGS
from forms import SettingsForm
from servers.models import Server
from music.models import Music, Request
import simplejson as json


@admin_only
@render_to('admin_panel.html')
def index(request):
    title = "Administration"
    icon = "cogs"
    user_count = User.objects.count()
    server_approval_count = Server.objects.filter(mod_approved=False).count()
    music_request_count = Request.objects.filter(fulfilled=False).count()
    return locals()


@admin_only
@render_to('simple_layouts/form_for_content.html')
def settings(request):
    title = "System Settings"
    icon = "cogs"
    form = SettingsForm()
    return locals()


@admin_only
@require_POST
def save_settings(request):
    if request.POST.get('save_changes'):
        for i,key in enumerate(PYPARTY_SETTINGS):
            save_setting(key, request.POST.get(key,'0'))
        messages.success(request, "Your settings were saved successfully!")
    return HttpResponseRedirect('/admin/')