from django.db import models

class Tecnology(models.Model):
    pass

class Location(models.Model):
    pass

class App(models.Model):
    name     = models.CharField(unique=True, max_length=50, verbose_name="App")

class Action(models.Model):
    name     = models.CharField(unique=True, max_length=50, verbose_name="Modulo")
    app      = models.ForeignKey(App, on_delete=models.CASCADE)

class Profile(models.Model):
    name     = models.CharField(unique=True, max_length=50, verbose_name="Nombre del perfil")

class User(models.Model):
    username = models.EmailField(unique=True, verbose_name="Nombre de usuario")
    password = models.CharField(max_length=50, verbose_name="Constraseña")
    name     = models.CharField(max_length=100, verbose_name="Nombres")
    lastname = models.CharField(max_length=100, verbose_name="Apellidos")
    active   = models.BooleanField(verbose_name="Activo/Inactivo") 
    profile  = models.ForeignKey(Profile, on_delete=models.DO_NOTHING)

class UserDeveloper(models.Model):
    username    = models.ForeignKey(User, on_delete=models.CASCADE)
    location    = models.ForeignKey('Location', on_delete=models.DO_NOTHING)

class DeveloperTecnologies(models.Model):
    developer   = models.ForeignKey(UserDeveloper, on_delete=models.CASCADE)
    tecnology   = models.ForeignKey('Tecnology', on_delete=models.CASCADE)
    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['developer', 'tecnology'], name="DeveloperTecnology")
        ]

class ProfilePermissions(models.Model):
    profile    = models.ForeignKey(Profile, on_delete=models.CASCADE)
    action     = models.ForeignKey(Action, on_delete=models.CASCADE)
    permission = models.BooleanField(verbose_name="Estado")

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['profile', 'action'], name="ProfileAction")
        ]