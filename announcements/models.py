from django.db import models
from accounts.models import User


class Announcement(models.Model):
    title = models.CharField(max_length=255)
    body = models.TextField()
    author = models.ForeignKey(User)
    posted_on = models.DateTimeField(auto_now_add=True)

    @staticmethod
    def latest(count):
        return Announcement.objects.order_by("posted_on")[:count]