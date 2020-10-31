from django.db import models
from form_creator.models import Form, Question, Answer
# Create your models here.
class CampaignForm(models.Model):
    """Class for CampaignForm model"""
    name = models.TextField()
    type_campaign = models.IntegerField(null=False)
    isabel_campaign = models.IntegerField(null=False)
    form = models.ForeignKey(Form, null=False, on_delete=models.DO_NOTHING)

class DataLlamada(models.Model):
    """Model for data llamada"""
    telefono = models.TextField(null=False)
    name = models.TextField(null=True)
    cedula = models.TextField(null=True)
    correo = models.EmailField(null=True)
    placa = models.TextField(null=True)
    linea_veh = models.TextField(null=True)

class AnswersHeader(models.Model):
    """Class for answer header"""
    campaing = models.ForeignKey(CampaignForm, on_delete=models.CASCADE)
    tercero = models.IntegerField(null=True)
    agente = models.IntegerField(null=True)
    call_id = models.IntegerField(null=True)
    data_llamada = models.ForeignKey(DataLlamada, null=True, on_delete=models.CASCADE)

class AnswersBody(models.Model):
    """Class for answers body"""
    header = models.ForeignKey(AnswersHeader, on_delete=models.CASCADE)
    question = models.ForeignKey(Question, on_delete=models.SET_NULL, null=True)
    question_text = models.TextField()
    answer = models.ForeignKey(Answer, on_delete=models.SET_NULL, null=True)
    answer_text = models.TextField()
