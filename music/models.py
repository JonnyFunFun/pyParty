from django.db import models
from django.contrib.auth.models import User


# Create your models here.
class Request(models.Model):
    requester = models.ForeignKey(User)
    song = models.ForeignKey('Music')
    votes = models.IntegerField(default=1)
    received_at = models.DateTimeField(auto_now_add=True)
    fulfilled = models.BooleanField(default=False)


class MusicSource(models.Model):
    path = models.CharField(max_length=255)


class Music(models.Model):
    artist = models.CharField(max_length=128)
    album = models.CharField(max_length=128)
    title = models.CharField(max_length=128)
    source = models.ForeignKey(MusicSource)
    filename = models.CharField(max_length=255)
    playing = models.BooleanField(default=False, db_index=True)

    @staticmethod
    def next_song_and_request():
        requests = Request.objects.filter(fulfilled=False).order_by('-votes', 'received_at',)
        if requests.count() != 0:
            return requests[0].song, requests[0]
        else:
            # return a random song
            return Music.objects.order_by('?')[0], None

    @staticmethod
    def currently_playing():
        try:
            return Music.objects.get(playing=True)
        except Music.DoesNotExist:
            return None

    def request(self, user):
        try:
            # try an active request
            request = Request.objects.get(fulfilled=False, song=self)
        except Request.DoesNotExist:
            # create a new one
            request = Request()
            request.requester = user
            request.song = self
        request.votes += 1
        request.save()