# Generated by Django 3.0.4 on 2020-06-02 01:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('profiles', '0003_app_label'),
    ]

    operations = [
        migrations.AlterField(
            model_name='action',
            name='name',
            field=models.CharField(max_length=50, unique=True, verbose_name='Modulo'),
        ),
    ]