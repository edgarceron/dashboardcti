"""Manages the models for the motivos app"""
from django.db import models

# Create your models here.
class Motivo(models.Model):
    """Class for motivos model"""
    name = models.CharField(unique=True, max_length=50, verbose_name="App")
    active = models.BooleanField(verbose_name="Activo/Inactivo", null=False, default=True)
