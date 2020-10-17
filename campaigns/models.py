from django.db import models
from form_creator.models import Form, Question, Answer
# Create your models here.
class CampaignForm(models.Model):
    """Class for CampaignForm model"""
    name = models.TextField()
    type_campaign = models.IntegerField(null=False)
    isabel_campaign = models.IntegerField(null=False)
    form = models.ForeignKey(Form, null=False, on_delete=models.DO_NOTHING)

class AnswersHeader(models.Model):
    """Class for answer header"""
    campaing = models.ForeignKey(CampaignForm, on_delete=models.CASCADE)
    tercero = models.IntegerField(null=False)

class AnswersBody(models.Model):
    """Class for answers body"""
    header = models.ForeignKey(AnswersHeader, on_delete=models.CASCADE)
    question = models.ForeignKey(Question, on_delete=models.SET_NULL, null=True)
    question_text = models.TextField()
    answer = models.ForeignKey(Answer, on_delete=models.SET_NULL, null=True)
    answer_text = models.TextField()
