"""Models for the maingui app"""
from django.db import models

# Create your models here.

class LoginSession(models.Model):
    key = models.CharField(unique=True, null=False, max_length=32)
    life = models.DateTimeField(null=False)
    profile = models.IntegerField(null=False)
