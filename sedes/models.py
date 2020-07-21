"""Manages the models for the sedes app"""
from django.db import models

# Create your models here.
class Sede(models.Model):
    "Model for an sede"
    name = models.CharField(max_length=50, null=False)
    address = models.CharField(max_length=100, null=False)
    active = models.BooleanField(verbose_name="Activo/Inactivo", null=False, default=True)
