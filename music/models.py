from django.db import models
from django.contrib.auth.models import User
import os

# Create your models here.
class MusicSource(models.Model):
    path = models.CharField(max_length=255)

class Music(models.Model):
    artist = models.CharField(max_length=128)
    album = models.CharField(max_length=128)
    title = models.CharField(max_length=128)
    source = models.ForeignKey(MusicSource)
    filename = models.CharField(max_length=255)

class Request(models.Model):
    requester = models.ForeignKey(User)
    song = models.ForeignKey(Music)
    votes = models.IntegerField(default=1)
    received_at = models.DateTimeField(auto_now_add=True)