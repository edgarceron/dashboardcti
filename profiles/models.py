"""Models for the profile app"""
from django.db import models
from django.db.models import Q

class App(models.Model):
    name = models.CharField(unique=True, max_length=50, verbose_name="App")

class Action(models.Model):
    name = models.CharField(max_length=50, verbose_name="Modulo")
    label = models.CharField(max_length=150, verbose_name="Etiqueta")
    app = models.ForeignKey(App, on_delete=models.CASCADE)

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['app', 'name'], name="AppAction")
        ]

class Profile(models.Model):
    name = models.CharField(unique=True, max_length=50, verbose_name="Nombre del perfil")
    active = models.BooleanField(verbose_name="Activo/Inactivo", null=False)

    @staticmethod
    def profilePickerFilter(value):
        return list(Profile.objects.filter(
            Q(active=True),
            Q(name__contains=value)
        )[:10])

    @staticmethod
    def profiles_listing_filter(search, start, length, count=False):
        """Filters the corresponding models given a search string"""
        if count:
            return Profile.objects.filter(
                Q(name__contains=search)
            ).count()
        else:
            return Profile.objects.filter(
                Q(name__contains=search)
            )[start:start + length]

class ProfilePermissions(models.Model):
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE)
    action = models.ForeignKey(Action, on_delete=models.CASCADE)
    permission = models.BooleanField(verbose_name="Estado")

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['profile', 'action'], name="ProfileAction")
        ]
# Create your models here.
