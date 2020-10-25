# Generated by Django 3.0.7 on 2020-10-25 00:05

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('campaigns', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='DataLlamada',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('telefono', models.TextField()),
                ('name', models.TextField(null=True)),
                ('cedula', models.TextField(null=True)),
                ('correo', models.EmailField(max_length=254, null=True)),
                ('placa', models.TextField(null=True)),
                ('linea_veh', models.TextField(null=True)),
            ],
        ),
        migrations.AddField(
            model_name='answersheader',
            name='agente',
            field=models.IntegerField(null=True),
        ),
        migrations.AddField(
            model_name='answersheader',
            name='call_id',
            field=models.IntegerField(null=True),
        ),
        migrations.AlterField(
            model_name='answersheader',
            name='tercero',
            field=models.IntegerField(null=True),
        ),
        migrations.AddField(
            model_name='answersheader',
            name='data_llamada',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='campaigns.DataLlamada'),
        ),
    ]
