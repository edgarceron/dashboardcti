from django.db import models
from form_creator.models import Form
# Create your models here.
class CampaignForm(models.Model):
    """Class for CampaignForm model"""
    isabelCampaign = models.IntegerField(unique=True, null=False)
    form = models.ForeignKey(Form, null=False, on_delete=models.DO_NOTHING)

class answersHeader(models.Model):
    campaing = models.ForeignKey(CampaignForm, on_delete=models.CASCADE)
    tercero = models.IntegerField(null=False)
    