from django.db import models

# list of settings and their defaults
PYPARTY_SETTINGS = {
    'site_name': 'pyParty LAN Party',
    'welcome_msg': 'Welcome to a pyParty-powered LAN!',
    'site_title': '<span class="color-teal">py</span>Party',
    'lan_name': 'pyParty',
    'enable_music': '1',
    'enable_benchmarks': '1',
    'enable_gallery': '1',
    'enable_tournaments': '1',
    'enable_servers': '1',
    'enable_noms': '1'
}


class Setting(models.Model):
    name = models.CharField(max_length=64,primary_key=True)
    value = models.CharField(max_length=128,null=True)