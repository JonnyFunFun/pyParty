from django.db import models
from django.contrib.auth.models import User
from math import ceil, log


class Tournament(models.Model):
    name = models.CharField(max_length=128)
    game = models.CharField(max_length=128)
    starts = models.DateTimeField()
    ends = models.DateTimeField()

    @property
    def bracket_depth(self):
        return ceil(log(self.teams.count() / 2, 2))

    def seed_matches(self, depth):
        pass  # TODO


class Team(models.Model):
    name = models.CharField(max_length=128)
    tournament = models.ForeignKey(Tournament, related_name='teams')
    players = models.ManyToManyField(User, related_name='tournaments')
    ready = models.BooleanField(default=False)
    seed = models.IntegerField(null=True)


RESULTS = (
    ('UP', 'Unplayed'),
    ('IP, ''In Progress'),
    ('BW', 'Bottom Win'),
    ('TW', 'Top Win'),
    ('BF', 'Bottom Forfeit'),
    ('TF', 'Top Forefeit')
)


class Match(models.Model):
    tournament = models.ForeignKey(Tournament, related_name='matches')
    top_team = models.ForeignKey(Team)
    bot_team = models.ForeignKey(Team)
    result = models.CharField(max_length=2, choices=RESULTS, default='UP')
    seed_depth = models.IntegerField()