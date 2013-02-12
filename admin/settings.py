from models import Setting

SETTING_DEFAULTS = {
    'site_name': 'pyParty LAN Party',
    'welcome_msg': 'Welcome to a pyParty-powered LAN!',
    'site_title': '<span class="color-teal">py</span>Party',
    'lan_name': 'pyParty'
}

def get_setting(name):
    try:
        setting = Setting.objects.get(name=name)
    except Setting.DoesNotExist:
        # save the default record for this item
        setting = Setting()
        setting.name = name
        setting.value = SETTING_DEFAULTS[name]
        setting.save()
    return setting.value