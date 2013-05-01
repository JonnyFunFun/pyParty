from django.db import models
from django.contrib.auth.models import User


RATING_CHOICES = (
    ('1', '1 - Terrible'),
    ('2', '2 - It was okay'),
    ('3', '3 - Not great, not bad'),
    ('4', '4 - Excellent'),
    ('5', '5 - Absolutely fantastic!')
)


class SurveyEntry(models.Model):
    user = models.ForeignKey(User, related_name="survey")
    lan_rating = models.IntegerField(blank=True, null=True, choices=RATING_CHOICES,
                                     help_text="How would you rate the LAN overall?", verbose_name="")
    pyp_rating = models.IntegerField(blank=True, null=True, choices=RATING_CHOICES,
                                     help_text="How would you rate the pyParty system?", verbose_name="")
    improvements = models.TextField(blank=True, null=True, help_text="What would you like to see improved?",
                                    verbose_name="")
    complaints = models.TextField(blank=True, null=True, help_text="What were your major complaints?", verbose_name="")
    praises = models.TextField(blank=True, null=True, help_text="What would you say was the best part of the LAN?")
    returning = models.BooleanField(blank=True, null=True, verbose_name="Would you return?")