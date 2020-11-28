"""Manages the models for the asesores app"""
from django.db import models
from sedes.models import Sede

# Create your models here.
class Asesor(models.Model):
    """Class for asesor model"""
    name = models.CharField(unique=True, max_length=100, verbose_name="App")
    active = models.BooleanField(verbose_name="Activo/Inactivo", null=False, default=True)
    asesor_dms = models.IntegerField(null=True, default=0)
