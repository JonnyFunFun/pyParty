from django.db import models
from django.contrib.auth.models import User
from math import ceil, log
from django.db.models import Q
from django.core.validators import MinValueValidator, MaxValueValidator


TOURNAMENT_MODES = (
    ('SE', 'Single Elimination'),
    ('DE', 'Double Elimination'),
    ('XX', 'Custom')
)


class Tournament(models.Model):
    name = models.CharField(max_length=128)
    game = models.CharField(max_length=128)
    starts = models.DateTimeField()
    ends = models.DateTimeField()
    team_size = models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(16)])
    max_teams = models.IntegerField(null=True)

    @property
    def bracket_depth(self):
        return int(ceil(log(self.teams.count() / 2, 2)))

    @property
    def total_seeds(self):
        return int(ceil(self.teams.count() / 2))
    
    @property
    def team_count(self):
        return self.teams.count()

    @staticmethod
    def team_array_seed_sort(left, right):
        return left.seed > right.seed

    def seed_matches(self, depth):
        if depth is 1:
            # populate the top-level of the brackets
            for side in ['R','L']:
                for seed in range(1, (self.total_seeds / 2)):
                    match = Match()
                    match.tournament = self
                    match.seed_depth = depth
                    match.bracket_side = side
                    match.top_team = self.teams.get(side=side, seed=seed)
                    match.bot_team = self.teams.get(side=side, seed=(self.total_seeds - (seed - 1)))
                    match.save()
        else:
            # populate a lower depth - we must base this off of winners of the previous seed
            for side in ['R','L']:
                teams = []
                matches = self.matches.filter(seed_depth=(depth - 1), bracket_side=side)
                for match in matches:
                    if match.result == 'BW' or 'TF':
                        teams.append(match.bot_team)
                    elif match.result == 'TW' or 'BF':
                        teams.append(match.top_team)
                # rearrange
                teams.sort(Tournament.team_array_seed_sort)
                for seed in range(1, (teams.__len__() / 2)):
                    match = Match()
                    match.tournament = self
                    match.seed_depth = seed
                    match.bracket_side = side
                    match.top_team = teams[seed-1]
                    match.bot_team = teams[-seed]
                    match.save()

    def random_populate_bracket(self):
        self.teams.update(seed=None, bracket_side='N')
        for side in ['R','L']:
            for seed in range(1, self.total_seeds):
                team = self.teams.filter(seed=None).order_by('?')[0]
                team.seed = seed
                team.bracket_side = side
                team.save()


BRACKET_SIDES = (
    ('N', 'Not Specified'),
    ('R', 'Right'),
    ('L', 'Left')
)


class Team(models.Model):
    name = models.CharField(max_length=128)
    tournament = models.ForeignKey(Tournament, related_name='teams')
    players = models.ManyToManyField(User, related_name='tournaments')
    ready = models.BooleanField(default=False)
    seed = models.IntegerField(null=True)
    bracket_side = models.CharField(choices=BRACKET_SIDES, default='N', max_length=1)

    @property
    def matches(self):
        return Match.objects.filter(Q(top_team=self) | Q(bot_team=self))


RESULTS = (
    ('UP', 'Unplayed'),
    ('IP', 'In Progress'),
    ('BW', 'Bottom Win'),
    ('TW', 'Top Win'),
    ('BF', 'Bottom Forfeit'),
    ('TF', 'Top Forefeit')
)


class Match(models.Model):
    tournament = models.ForeignKey(Tournament, related_name='matches')
    top_team = models.ForeignKey(Team, related_name='+')
    bot_team = models.ForeignKey(Team, related_name='+')
    result = models.CharField(max_length=2, choices=RESULTS, default='UP')
    seed_depth = models.IntegerField()
    bracket_side = models.CharField(choices=BRACKET_SIDES, default='N', max_length=1)