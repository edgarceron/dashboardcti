from django.db import models
from django.db.models import Q
from profiles.models import Profile

class Tecnology(models.Model):
    pass

class Location(models.Model):
    pass

class User(models.Model):
    username     = models.EmailField(unique=True, verbose_name="Nombre de usuario", null=False, error_messages={'unique':'Ya existe un usuario registrado con este correo'})
    password     = models.CharField(max_length=50, verbose_name="Constraseña", null=False)
    name         = models.CharField(max_length=100, verbose_name="Nombres", null=False)
    lastname     = models.CharField(max_length=100, verbose_name="Apellidos", null=False)
    active       = models.BooleanField(verbose_name="Activo/Inactivo", null=False) 
    profile      = models.ForeignKey(Profile, on_delete=models.DO_NOTHING, null=True)
    needPassword = models.BooleanField(verbose_name="Cambiar contraseña", null=False, default=True)

    @staticmethod
    def usersPickerFilter(value):
        return list(User.objects.filter(
            Q(active = True), 
            Q(username__contains = value) | Q(name__contains = value) | Q(lastname__contains = value)
        )[:10])

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
