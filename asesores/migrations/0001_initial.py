# Generated by Django 3.0.7 on 2020-11-02 20:40

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('sedes', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Asesor',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100, unique=True, verbose_name='App')),
                ('active', models.BooleanField(default=True, verbose_name='Activo/Inactivo')),
                ('asesor_dms', models.IntegerField(default=0, null=True)),
                ('sede', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='sedes.Sede')),
            ],
        ),
    ]
