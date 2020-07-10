"""Contains the models for the form_creator app"""
from django.db import models
from django.db.models import Q

# Create your models here.
class Form(models.Model):
    "Model for an form"
    name = models.CharField(unique=True, max_length=50)

    @staticmethod
    def form_picker_filter(value):
        return list(Form.objects.filter(
            Q(active=True),
            Q(name__contains=value)
        )[:10])

    @staticmethod
    def form_listing_filter(search, start, length, count=False):
        """Filters the corresponding models given a search string"""
        if count:
            return Form.objects.filter(
                Q(name__contains=search)
            ).count()
        else:
            return Form.objects.filter(
                Q(name__contains=search)
            )[start:start + length]

class Question(models.Model):
    "Model for questions"
    text = models.TextField()
    """
    1. Falso o verdadero
    2. Texto
    3. Multiples opciones, una respuesta
    4. Multiples opciones, multiples respuestas
    """
    question_type = models.IntegerField()
    empty = models.BooleanField()

    class Meta:
        constraints = [
            models.CheckConstraint(
                check=Q(question_type__lte=4),
                name="question_type_upper"),
            models.CheckConstraint(
                check=Q(question_type__gte=1),
                name="question_type_lower"),
        ]

class Asnwer(models.Model):
    "Model for answers"
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    text = models.TextField()

class PollCampaing(models.Model):
    """Model for poll campaings """
    issabel_campaign = models.IntegerField(null=False, unique=True)
    form = models.ForeignKey(Form, on_delete=models.CASCADE, null=False)

class QuestionAnswers(models.Model):
    "Model for question answers"
    campaing = models.ForeignKey(PollCampaing, on_delete=models.CASCADE, null=False)
    client = models.CharField(max_length=20, null=False)
    question = models.ForeignKey(Question, on_delete=models.CASCADE, null=False)
    asnwer = models.ForeignKey(Asnwer, on_delete=models.CASCADE, null=True)
    text_answer = models.TextField(null=True)
    class Meta:
        constraints = [
            models.CheckConstraint(
                check=(Q(asnwer__isnull=False) | Q(text_answer__isnull=False)),
                name="answer_not_null")
        ]
