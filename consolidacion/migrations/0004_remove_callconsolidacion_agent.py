# Generated by Django 3.0.7 on 2020-07-27 01:05

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('consolidacion', '0003_callconsolidacion'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='callconsolidacion',
            name='agent',
        ),
    ]