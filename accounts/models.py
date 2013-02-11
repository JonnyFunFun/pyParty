from django.db import models
from django.contrib.auth.models import User
from django.utils.translation import ugettext as _
from userena.models import UserenaBaseProfile

class UserProfile(UserenaBaseProfile):
    class Meta:
        app_label = 'accounts'
    user = models.OneToOneField(User,
        unique=True,
        verbose_name=_('user'),
        related_name='my_profile')
    hostname = models.CharField(max_length=64)
