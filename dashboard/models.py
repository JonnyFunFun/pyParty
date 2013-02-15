from django.db import models
from django.contrib.auth.models import User


class News(models.Model):
    author = models.ForeignKey(User)
    title = models.CharField(max_length=255)
    body = models.TextField()
    posted_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name_plural = 'News'