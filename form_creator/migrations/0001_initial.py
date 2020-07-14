# Generated by Django 3.0.7 on 2020-07-11 21:57

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Answer',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('text', models.TextField()),
            ],
        ),
        migrations.CreateModel(
            name='Form',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50, unique=True)),
            ],
        ),
        migrations.CreateModel(
            name='PollCampaing',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('issabel_campaign', models.IntegerField(unique=True)),
            ],
        ),
        migrations.CreateModel(
            name='Question',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('text', models.TextField()),
                ('question_type', models.IntegerField()),
                ('empty', models.BooleanField()),
            ],
        ),
        migrations.CreateModel(
            name='QuestionAnswers',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('client', models.CharField(max_length=20)),
                ('text_answer', models.TextField(null=True)),
                ('asnwer', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='form_creator.Answer')),
                ('campaing', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='form_creator.PollCampaing')),
                ('question', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='form_creator.Question')),
            ],
        ),
        migrations.AddConstraint(
            model_name='question',
            constraint=models.CheckConstraint(check=models.Q(question_type__lte=4), name='question_type_upper'),
        ),
        migrations.AddConstraint(
            model_name='question',
            constraint=models.CheckConstraint(check=models.Q(question_type__gte=1), name='question_type_lower'),
        ),
        migrations.AddField(
            model_name='pollcampaing',
            name='form',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='form_creator.Form'),
        ),
        migrations.AddField(
            model_name='answer',
            name='question',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='form_creator.Question'),
        ),
        migrations.AddConstraint(
            model_name='questionanswers',
            constraint=models.CheckConstraint(check=models.Q(('asnwer__isnull', False), ('text_answer__isnull', False), _connector='OR'), name='answer_not_null'),
        ),
    ]
