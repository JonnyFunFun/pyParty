from decorators import admin_only
from global_decorators import render_to
from django.contrib.auth.models import User
from django.views.decorators.http import require_POST
from django.http import HttpResponseRedirect
from django.contrib import messages
from settings import save_setting
from models import PYPARTY_SETTINGS
from forms import SettingsForm

@admin_only
@render_to('admin_panel.html')
def index(request):
    title = "Administration"
    icon = "cogs"
    user_count = User.objects.count()
    return locals()

@admin_only
@render_to('settings.html')
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