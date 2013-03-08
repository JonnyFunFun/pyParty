from django.db import models
from django.db.models import Count
from django.contrib.auth.models import User


# Create your models here.
class Request(models.Model):
    song = models.ForeignKey('Music')
    requester = models.ForeignKey(User)
    received_at = models.DateTimeField(auto_now_add=True)
    fulfilled = models.BooleanField(default=False)


class RequestVote(models.Model):
    requester = models.ForeignKey(User)
    request = models.ForeignKey(Request)


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
        requests = Request.objects.filter(fulfilled=False)
        requests = requests.annotate(vote_count=Count('requestvote'))
        requests = requests.order_by('-vote_count', 'received_at',)
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


    @property
    def associated_request(self):
        try:
            return Request.objects.get(fulfilled=False, song=self)
        except Request.DoesNotExist:
            return None


    def request(self, user):
        # try an active request
        if self.associated_request is None:
            # create a new one
            request = Request()
            request.requester = user
            request.song = self
            request.save()
            vote = RequestVote()
            vote.request = request
            vote.requester = user
            vote.save()
        if self.associated_request.requester != user:
            try:
                RequestVote.objects.get(request=self.associated_request, requester=user)
            except RequestVote.DoesNotExist:
                # good to create it
                vote = RequestVote()
                vote.request = self.associated_request
                vote.requester = user

    @property
    def vote_count(self):
        request = self.associated_request
        if request is None:
            return 0
        return request.requestvote_set.count()