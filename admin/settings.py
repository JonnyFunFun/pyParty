from admin.models import Setting, PYPARTY_SETTINGS


def get_setting(name):
    try:
        setting = Setting.objects.get(name=name)
    except Setting.DoesNotExist:
        # save the default record for this item
        setting = Setting()
        setting.name = name
        setting.value = PYPARTY_SETTINGS[name]
        setting.save()
    return setting.value


def save_setting(name, value):
    try:
        setting = Setting.objects.get(name=name)
    except Setting.DoesNotExist:
        setting = Setting()
        setting.name = name
    if value == 'on':
        value = '1'
    setting.value = value
    setting.save()

TEMPLATE_DEBUG = True
