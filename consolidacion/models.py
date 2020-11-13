"""Manages the models for the consolidacion app"""
import os
from django.db import models
from django.utils import timezone
from users.models import User
from sedes.models import Sede
from motivos.models import Motivo
# Create your models here.
class Consolidacion(models.Model):
    """Class for consolidacion model"""
    cedula = models.CharField(max_length=20, null=False)
    placa = models.CharField(max_length=10, null=False)
    fecha = models.DateField(null=False)
    motivo = models.ForeignKey(Motivo, on_delete=models.DO_NOTHING, null=False)
    sede = models.ForeignKey(Sede, on_delete=models.CASCADE, null=True)

def upload_to(instance, filename):
    now = timezone.now()
    base, extension = os.path.splitext(filename.lower())
    return f"uploads/consolidaciones{now:%Y%m%d%H%M%S}{extension}"

class ConsolidacionFileUploads(models.Model):
    """Class for the consolidacion csv uploads"""
    file = models.FileField(upload_to=upload_to, null=False)

class CallConsolidacion(models.Model):
    """Class for the calls made for consolidacion"""
    consolidacion = models.OneToOneField(Consolidacion, null=False, on_delete=models.CASCADE)
    call = models.IntegerField(null=False, unique=True)
    cita_tall_id = models.IntegerField(null=True, unique=True)
    cita_crm_id = models.IntegerField(null=True, unique=True)
    call_made = models.BooleanField(null=False, default=False)
    observaciones = models.TextField(null=True)

