from models import Setting, SETTING_DEFAULTS

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