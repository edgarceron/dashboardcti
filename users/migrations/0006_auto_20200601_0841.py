# Generated by Django 3.0.4 on 2020-06-01 13:41

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0005_auto_20200530_1839'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='loginsession',
            name='profile',
        ),
        migrations.AddField(
            model_name='loginsession',
            name='user',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.DO_NOTHING, to='users.User'),
        ),
    ]
