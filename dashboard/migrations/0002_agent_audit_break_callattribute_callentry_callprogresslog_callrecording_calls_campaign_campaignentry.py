# Generated by Django 3.0.4 on 2020-06-02 03:10

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('dashboard', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Agent',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('type', models.CharField(max_length=5)),
                ('number', models.CharField(max_length=40)),
                ('name', models.CharField(max_length=250)),
                ('password', models.CharField(max_length=250)),
                ('estatus', models.CharField(blank=True, max_length=1, null=True)),
                ('eccp_password', models.CharField(blank=True, max_length=128, null=True)),
            ],
            options={
                'db_table': 'agent',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='Audit',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('datetime_init', models.DateTimeField()),
                ('datetime_end', models.DateTimeField(blank=True, null=True)),
                ('duration', models.TimeField(blank=True, null=True)),
                ('ext_parked', models.CharField(blank=True, max_length=10, null=True)),
            ],
            options={
                'db_table': 'audit',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='Break',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=250)),
                ('description', models.CharField(blank=True, max_length=250, null=True)),
                ('status', models.CharField(max_length=1)),
                ('tipo', models.CharField(blank=True, max_length=1, null=True)),
            ],
            options={
                'db_table': 'break',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='CallAttribute',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('columna', models.CharField(blank=True, max_length=30, null=True)),
                ('value', models.CharField(max_length=128)),
                ('column_number', models.PositiveIntegerField()),
            ],
            options={
                'db_table': 'call_attribute',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='CallEntry',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('callerid', models.CharField(max_length=15)),
                ('datetime_init', models.DateTimeField(blank=True, null=True)),
                ('datetime_end', models.DateTimeField(blank=True, null=True)),
                ('duration', models.PositiveIntegerField(blank=True, null=True)),
                ('status', models.CharField(blank=True, max_length=32, null=True)),
                ('transfer', models.CharField(blank=True, max_length=6, null=True)),
                ('datetime_entry_queue', models.DateTimeField(blank=True, null=True)),
                ('duration_wait', models.IntegerField(blank=True, null=True)),
                ('uniqueid', models.CharField(blank=True, max_length=32, null=True)),
                ('trunk', models.CharField(max_length=20)),
            ],
            options={
                'db_table': 'call_entry',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='CallProgressLog',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('datetime_entry', models.DateTimeField()),
                ('new_status', models.CharField(max_length=32)),
                ('retry', models.PositiveIntegerField(blank=True, null=True)),
                ('uniqueid', models.CharField(blank=True, max_length=32, null=True)),
                ('trunk', models.CharField(blank=True, max_length=20, null=True)),
                ('duration', models.PositiveIntegerField(blank=True, null=True)),
            ],
            options={
                'db_table': 'call_progress_log',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='CallRecording',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('datetime_entry', models.DateTimeField()),
                ('uniqueid', models.CharField(max_length=32)),
                ('channel', models.CharField(max_length=80)),
                ('recordingfile', models.CharField(blank=True, max_length=255, null=True)),
            ],
            options={
                'db_table': 'call_recording',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='Calls',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('phone', models.CharField(max_length=32)),
                ('status', models.CharField(blank=True, max_length=32, null=True)),
                ('uniqueid', models.CharField(blank=True, max_length=32, null=True)),
                ('fecha_llamada', models.DateTimeField(blank=True, null=True)),
                ('start_time', models.DateTimeField(blank=True, null=True)),
                ('end_time', models.DateTimeField(blank=True, null=True)),
                ('retries', models.PositiveIntegerField()),
                ('duration', models.PositiveIntegerField(blank=True, null=True)),
                ('transfer', models.CharField(blank=True, max_length=6, null=True)),
                ('datetime_entry_queue', models.DateTimeField(blank=True, null=True)),
                ('duration_wait', models.IntegerField(blank=True, null=True)),
                ('dnc', models.IntegerField()),
                ('date_init', models.DateField(blank=True, null=True)),
                ('date_end', models.DateField(blank=True, null=True)),
                ('time_init', models.TimeField(blank=True, null=True)),
                ('time_end', models.TimeField(blank=True, null=True)),
                ('agent', models.CharField(blank=True, max_length=32, null=True)),
                ('failure_cause', models.PositiveIntegerField(blank=True, null=True)),
                ('failure_cause_txt', models.CharField(blank=True, max_length=32, null=True)),
                ('datetime_originate', models.DateTimeField(blank=True, null=True)),
                ('trunk', models.CharField(blank=True, max_length=20, null=True)),
                ('scheduled', models.IntegerField()),
            ],
            options={
                'db_table': 'calls',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='Campaign',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=64)),
                ('datetime_init', models.DateField()),
                ('datetime_end', models.DateField()),
                ('daytime_init', models.TimeField()),
                ('daytime_end', models.TimeField()),
                ('retries', models.PositiveIntegerField()),
                ('trunk', models.CharField(blank=True, max_length=255, null=True)),
                ('context', models.CharField(max_length=32)),
                ('queue', models.CharField(max_length=16)),
                ('max_canales', models.PositiveIntegerField()),
                ('num_completadas', models.PositiveIntegerField(blank=True, null=True)),
                ('promedio', models.PositiveIntegerField(blank=True, null=True)),
                ('desviacion', models.PositiveIntegerField(blank=True, null=True)),
                ('script', models.TextField()),
                ('estatus', models.CharField(max_length=1)),
            ],
            options={
                'db_table': 'campaign',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='CampaignEntry',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=64)),
                ('datetime_init', models.DateField()),
                ('datetime_end', models.DateField()),
                ('daytime_init', models.TimeField()),
                ('daytime_end', models.TimeField()),
                ('estatus', models.CharField(max_length=1)),
                ('script', models.TextField()),
            ],
            options={
                'db_table': 'campaign_entry',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='CampaignExternalUrl',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('urltemplate', models.CharField(max_length=250)),
                ('description', models.CharField(max_length=64)),
                ('active', models.IntegerField()),
                ('opentype', models.CharField(max_length=16)),
            ],
            options={
                'db_table': 'campaign_external_url',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='Contact',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('cedula_ruc', models.CharField(max_length=15)),
                ('name', models.CharField(max_length=50)),
                ('telefono', models.CharField(max_length=15)),
                ('apellido', models.CharField(max_length=50)),
                ('origen', models.CharField(blank=True, max_length=4, null=True)),
            ],
            options={
                'db_table': 'contact',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='CurrentCallEntry',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('callerid', models.CharField(max_length=15)),
                ('datetime_init', models.DateTimeField()),
                ('uniqueid', models.CharField(blank=True, max_length=32, null=True)),
                ('channelclient', models.CharField(blank=True, db_column='ChannelClient', max_length=32, null=True)),
                ('hold', models.CharField(blank=True, max_length=1, null=True)),
            ],
            options={
                'db_table': 'current_call_entry',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='CurrentCalls',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('fecha_inicio', models.DateTimeField()),
                ('uniqueid', models.CharField(blank=True, max_length=32, null=True)),
                ('queue', models.CharField(max_length=16)),
                ('agentnum', models.CharField(max_length=16)),
                ('event', models.CharField(max_length=32)),
                ('channel', models.CharField(db_column='Channel', max_length=32)),
                ('channelclient', models.CharField(blank=True, db_column='ChannelClient', max_length=32, null=True)),
                ('hold', models.CharField(blank=True, max_length=1, null=True)),
            ],
            options={
                'db_table': 'current_calls',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='DontCall',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('caller_id', models.CharField(max_length=15)),
                ('date_income', models.DateTimeField(blank=True, null=True)),
                ('status', models.CharField(blank=True, max_length=1, null=True)),
            ],
            options={
                'db_table': 'dont_call',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='EccpAuthorizedClients',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('username', models.CharField(max_length=64)),
                ('md5_password', models.CharField(max_length=32)),
            ],
            options={
                'db_table': 'eccp_authorized_clients',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='Form',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre', models.CharField(max_length=40)),
                ('descripcion', models.CharField(max_length=150)),
                ('estatus', models.CharField(max_length=1)),
            ],
            options={
                'db_table': 'form',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='FormDataRecolected',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('value', models.CharField(max_length=250)),
            ],
            options={
                'db_table': 'form_data_recolected',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='FormDataRecolectedEntry',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('value', models.CharField(max_length=250)),
            ],
            options={
                'db_table': 'form_data_recolected_entry',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='FormField',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('etiqueta', models.TextField()),
                ('value', models.TextField()),
                ('tipo', models.CharField(max_length=25)),
                ('orden', models.PositiveIntegerField()),
            ],
            options={
                'db_table': 'form_field',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='QueueCallEntry',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('queue', models.CharField(blank=True, max_length=50, null=True)),
                ('date_init', models.DateField(blank=True, null=True)),
                ('time_init', models.TimeField(blank=True, null=True)),
                ('date_end', models.DateField(blank=True, null=True)),
                ('time_end', models.TimeField(blank=True, null=True)),
                ('estatus', models.CharField(max_length=1)),
                ('script', models.TextField(blank=True, null=True)),
            ],
            options={
                'db_table': 'queue_call_entry',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='ValorConfig',
            fields=[
                ('config_key', models.CharField(max_length=32, primary_key=True, serialize=False)),
                ('config_value', models.CharField(max_length=128)),
                ('config_blob', models.TextField(blank=True, null=True)),
            ],
            options={
                'db_table': 'valor_config',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='CampaignForm',
            fields=[
                ('id_campaign', models.OneToOneField(db_column='id_campaign', on_delete=django.db.models.deletion.DO_NOTHING, primary_key=True, serialize=False, to='dashboard.Campaign')),
            ],
            options={
                'db_table': 'campaign_form',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='CampaignFormEntry',
            fields=[
                ('id_campaign', models.OneToOneField(db_column='id_campaign', on_delete=django.db.models.deletion.DO_NOTHING, primary_key=True, serialize=False, to='dashboard.CampaignEntry')),
            ],
            options={
                'db_table': 'campaign_form_entry',
                'managed': False,
            },
        ),
    ]
