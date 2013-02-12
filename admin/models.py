from django.db import models

# Create your models here.
class Setting(models.Model):
    name = models.CharField(max_length=64,primary_key=True)
    value = models.CharField(max_length=128,null=True)