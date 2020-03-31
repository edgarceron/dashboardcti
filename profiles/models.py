from django.db import models

class App(models.Model):
    name     = models.CharField(unique=True, max_length=50, verbose_name="App")

class Action(models.Model):
    name     = models.CharField(max_length=50, verbose_name="Modulo")
    label    = models.CharField(max_length=150, verbose_name="Etiqueta")
    app      = models.ForeignKey(App, on_delete=models.CASCADE)

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['app', 'name'], name="AppAction")
        ]

class Profile(models.Model):
    name     = models.CharField(unique=True, max_length=50, verbose_name="Nombre del perfil")

class ProfilePermissions(models.Model):
    profile    = models.ForeignKey(Profile, on_delete=models.CASCADE)
    action     = models.ForeignKey(Action, on_delete=models.CASCADE)
    permission = models.BooleanField(verbose_name="Estado")

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['profile', 'action'], name="ProfileAction")
        ]
# Create your models here.
