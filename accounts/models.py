from django.db import models
from django.contrib.auth.models import User
from django.utils.translation import ugettext as _
from rig_info import *

FLAG_ADMIN = 32
FLAG_OP = 16
FLAG_VIP = 8


class UserProfile(models.Model):
    class Meta:
        app_label = 'accounts'

    user = models.OneToOneField(User,
        unique=True,
        verbose_name=_('user'),
        related_name='my_profile')
    hostname = models.CharField(max_length=64)
    quote = models.CharField(max_length=255, blank=True)
    clan = models.CharField(max_length=64, blank=True)
    avatar = models.ImageField(upload_to=lambda p, f: "avatar%s_%s" % (p.user.id, f), blank=True)
    flags = models.IntegerField(default=0)

    about_me = models.TextField(blank=True)

    processor = models.CharField(max_length=3, choices=PROCESSOR_CHOICES, blank=True)
    processor_family = models.CharField(max_length=128, verbose_name="Family", blank=True)
    processor_speed = models.IntegerField(blank=True, null=True, verbose_name="Speed")

    graphics = models.CharField(max_length=2, choices=GFX_CHOICES, blank=True)
    graphics_model = models.CharField(max_length=128, verbose_name="Model", blank=True)
    graphics_memory = models.IntegerField(choices=GFX_MEMORY_CHOICES, verbose_name="Memory", blank=True, null=True)

    memory = models.IntegerField(blank=True, null=True)
    memory_type = models.CharField(max_length=4, choices=MEMORY_TYPE_CHOICES, verbose_name="Type", blank=True)

    hdd_space = models.IntegerField(blank=True, null=True, verbose_name="HDD Space")

    case =  models.CharField(max_length=128, blank=True)
    monitor = models.CharField(max_length=128, blank=True)

    comments = models.TextField(blank=True)

    @property
    def username(self):
        return self.user.username

    @property
    def first_name(self):
        return self.user.first_name

    @property
    def last_name(self):
        return self.user.last_name

    @property
    def admin(self):
        return self.is_flag(FLAG_ADMIN)

    @property
    def vip(self):
        return self.is_flag(FLAG_VIP)

    @property
    def operator(self):
        return self.is_flag(FLAG_OP)

    def is_flag(self, flag):
        return (self.flags & flag) != 0

    def set_flag(self, flag):
        if self.flags:
            self.flags = self.flags ^ flag
        else:
            self.flags = flag

    @property
    def full_handle(self):
        ret = ('%s "%s" %s' % (self.user.first_name, self.user.username, self.user.last_name)).strip(' \t\n\r')
        return ret.rstrip('"').lstrip('"')

    @property
    def chat_color(self):
        if self.is_flag(FLAG_ADMIN):
            return 'red'
        elif self.is_flag(FLAG_OP):
            return 'orange'
        elif self.is_flag(FLAG_VIP):
            return 'blue'
        return 'black'

# User => Profile shortcuts
User.profile = property(lambda u: UserProfile.objects.get_or_create(user=u)[0])
User.is_admin = property(lambda u: u.profile.admin)
User.is_operator = property(lambda u: u.profile.operator)
User.is_vip = property(lambda u: u.profile.vip)
User.full_handle = property(lambda u: u.profile.full_handle)