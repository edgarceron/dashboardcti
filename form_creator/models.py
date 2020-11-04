"""Contains the models for the form_creator app"""
from django.db import models
from django.db.models import Q

# Create your models here.
class Form(models.Model):
    "Model for an form"
    name = models.CharField(unique=True, max_length=50, error_messages={'unique':'Ya existe un formulario registrado con este nombre.'})

class Question(models.Model):
    "Model for questions"
    text = models.TextField()
    """
    1. Falso o verdadero
    2. Texto
    3. Multiples opciones, una respuesta
    4. Multiples opciones, multiples respuestas
    5. Fecha hora
    """
    question_type = models.IntegerField()
    empty = models.BooleanField()
    form = models.ForeignKey(Form, on_delete=models.CASCADE, null=False)
    position = models.IntegerField(null=False)

    class Meta:
        constraints = [
            models.CheckConstraint(
                check=Q(question_type__lte=5),
                name="question_type_upper"),
            models.CheckConstraint(
                check=Q(question_type__gte=1),
                name="question_type_lower"),
        ]

class Answer(models.Model):
    "Model for answers"
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    text = models.TextField()

class PollCampaign(models.Model):
    """Model for poll campaigns """
    issabel_campaign = models.IntegerField(null=False, unique=True)
    form = models.ForeignKey(Form, on_delete=models.CASCADE, null=False)

class QuestionAnswers(models.Model):
    "Model for question answers"
    campaign = models.ForeignKey(PollCampaign, on_delete=models.CASCADE, null=False)
    client = models.CharField(max_length=20, null=False)
    question = models.TextField()
    asnwer = models.TextField()
    text_answer = models.TextField(null=True)
    class Meta:
        constraints = [
            models.CheckConstraint(
                check=(Q(asnwer__isnull=False) | Q(text_answer__isnull=False)),
                name="answer_not_null")
        ]
