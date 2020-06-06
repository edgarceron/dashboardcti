# Generated by Django 3.0.4 on 2020-06-02 01:51

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='DatosPersonales',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombres', models.CharField(max_length=100, verbose_name='Nombres')),
                ('primer_apellido', models.CharField(max_length=50, verbose_name='Primer Apellido')),
                ('segundo_apellido', models.CharField(max_length=50, verbose_name='Segundo Apellido')),
                ('fecha_nacimiento', models.DateField(verbose_name='Fecha de nacimiento')),
                ('tipo_documento', models.CharField(max_length=50, verbose_name='Tipo de documento')),
                ('identificacion', models.CharField(max_length=50, verbose_name='Identificación')),
                ('telefono', models.CharField(max_length=50, verbose_name='Teléfono')),
                ('email', models.EmailField(max_length=100, verbose_name='Identificación')),
                ('direccion', models.CharField(max_length=100, null=True, verbose_name='Dirección')),
                ('departamento', models.CharField(max_length=100, null=True, verbose_name='Departamento')),
                ('barrio', models.CharField(max_length=100, null=True, verbose_name='Barrio')),
                ('municipio', models.CharField(max_length=100, null=True, verbose_name='Municipio')),
                ('tipo_servicio', models.CharField(max_length=100, null=True, verbose_name='Tipo de servicio')),
            ],
        ),
        migrations.CreateModel(
            name='Solicitud',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('fecha_recepcion', models.DateTimeField(verbose_name='Tipo de documento')),
                ('empresa', models.CharField(max_length=100, verbose_name='Empresa que registra')),
                ('quien_registra', models.CharField(max_length=100, verbose_name='Agente que registra')),
                ('informacion', models.TextField(verbose_name='Información adicional')),
                ('tipo_servicio', models.CharField(max_length=100, verbose_name='Tipo de servicio')),
                ('motivo_llamada', models.CharField(max_length=100, verbose_name='Motivo llamada')),
                ('solicitante', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='dashboard.DatosPersonales')),
            ],
        ),
    ]