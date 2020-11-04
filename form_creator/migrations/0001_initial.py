# Generated by Django 3.0.7 on 2020-11-03 15:53

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Form',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(error_messages={'unique': 'Ya existe un formulario registrado con este nombre.'}, max_length=50, unique=True)),
            ],
        ),
        migrations.CreateModel(
            name='PollCampaign',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('issabel_campaign', models.IntegerField(unique=True)),
                ('form', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='form_creator.Form')),
            ],
        ),
        migrations.CreateModel(
            name='QuestionAnswers',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('client', models.CharField(max_length=20)),
                ('question', models.TextField()),
                ('asnwer', models.TextField()),
                ('text_answer', models.TextField(null=True)),
                ('campaign', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='form_creator.PollCampaign')),
            ],
        ),
        migrations.CreateModel(
            name='Question',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('text', models.TextField()),
                ('question_type', models.IntegerField()),
                ('empty', models.BooleanField()),
                ('position', models.IntegerField()),
                ('form', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='form_creator.Form')),
            ],
        ),
        migrations.CreateModel(
            name='Answer',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('text', models.TextField()),
                ('question', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='form_creator.Question')),
            ],
        ),
        migrations.AddConstraint(
            model_name='questionanswers',
            constraint=models.CheckConstraint(check=models.Q(('asnwer__isnull', False), ('text_answer__isnull', False), _connector='OR'), name='answer_not_null'),
        ),
        migrations.AddConstraint(
            model_name='question',
            constraint=models.CheckConstraint(check=models.Q(question_type__lte=4), name='question_type_upper'),
        ),
        migrations.AddConstraint(
            model_name='question',
            constraint=models.CheckConstraint(check=models.Q(question_type__gte=1), name='question_type_lower'),
        ),
    ]
