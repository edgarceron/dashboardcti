# Generated by Django 3.0.4 on 2020-05-31 16:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('profiles', '0002_profile_active'),
    ]

    operations = [
        migrations.AddField(
            model_name='app',
            name='label',
            field=models.CharField(default='', max_length=100, verbose_name='Etiqueta'),
        ),
    ]
