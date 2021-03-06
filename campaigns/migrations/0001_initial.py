# Generated by Django 3.0.7 on 2020-11-03 16:19

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('form_creator', '0001_initial'),
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
        migrations.CreateModel(
            name='CampaignForm',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.TextField()),
                ('type_campaign', models.IntegerField()),
                ('isabel_campaign', models.IntegerField()),
                ('form', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='form_creator.Form')),
            ],
        ),
        migrations.CreateModel(
            name='AnswersHeader',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('tercero', models.IntegerField(null=True)),
                ('agente', models.IntegerField(null=True)),
                ('call_id', models.IntegerField(null=True)),
                ('campaign', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='campaigns.CampaignForm')),
                ('data_llamada', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='campaigns.DataLlamada')),
            ],
        ),
        migrations.CreateModel(
            name='AnswersBody',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('question_text', models.TextField()),
                ('answer_text', models.TextField()),
                ('answer', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='form_creator.Answer')),
                ('header', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='campaigns.AnswersHeader')),
                ('question', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='form_creator.Question')),
            ],
        ),
    ]
