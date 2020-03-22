# Generated by Django 3.0.4 on 2020-03-22 16:37

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Action',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50, unique=True, verbose_name='Modulo')),
            ],
        ),
        migrations.CreateModel(
            name='App',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50, unique=True, verbose_name='App')),
            ],
        ),
        migrations.CreateModel(
            name='Location',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
            ],
        ),
        migrations.CreateModel(
            name='Profile',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50, unique=True, verbose_name='Nombre del perfil')),
            ],
        ),
        migrations.CreateModel(
            name='Tecnology',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
            ],
        ),
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('username', models.EmailField(max_length=254, unique=True, verbose_name='Nombre de usuario')),
                ('password', models.CharField(max_length=50, verbose_name='Constraseña')),
                ('name', models.CharField(max_length=100, verbose_name='Nombres')),
                ('lastname', models.CharField(max_length=100, verbose_name='Apellidos')),
                ('active', models.BooleanField(verbose_name='Activo/Inactivo')),
                ('profile', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='users.Profile')),
            ],
        ),
        migrations.CreateModel(
            name='UserDeveloper',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('location', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='users.Location')),
                ('username', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='users.User')),
            ],
        ),
        migrations.CreateModel(
            name='ProfilePermissions',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('permission', models.BooleanField(verbose_name='Estado')),
                ('action', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='users.Action')),
                ('profile', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='users.Profile')),
            ],
        ),
        migrations.CreateModel(
            name='DeveloperTecnologies',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('developer', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='users.UserDeveloper')),
                ('tecnology', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='users.Tecnology')),
            ],
        ),
        migrations.AddField(
            model_name='action',
            name='app',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='users.App'),
        ),
        migrations.AddConstraint(
            model_name='profilepermissions',
            constraint=models.UniqueConstraint(fields=('profile', 'action'), name='ProfileAction'),
        ),
        migrations.AddConstraint(
            model_name='developertecnologies',
            constraint=models.UniqueConstraint(fields=('developer', 'tecnology'), name='DeveloperTecnology'),
        ),
    ]
