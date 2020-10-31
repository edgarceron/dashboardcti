"""Contains the serializers for the users module"""
from rest_framework import serializers
from .models import UserAgent, Agent, UserSede, Campaign, Calls, CallEntry, CurrentCallEntry, CampaignEntry

class AgentSerializer(serializers.ModelSerializer):
    """Serializer for Agent model"""
    class Meta:
        model = Agent
        fields = ['id', 'number', 'name']

class UserAgentSerializer(serializers.ModelSerializer):
    """Serializer for UserAgent model"""
    class Meta:
        model = UserAgent
        fields = ['id', 'user', 'agent']

    def create(self, validated_data):
        user_obj = UserAgent(**validated_data)
        user_obj.save()
        return user_obj

    def update(self, instance, validated_data):
        instance.user = validated_data["user"]
        instance.agent = validated_data["agent"]
        instance.save()
        return instance

class UserSedeSerializer(serializers.ModelSerializer):
    """Serializer for UserAgent model"""
    class Meta:
        model = UserSede
        fields = ['id', 'user', 'sede']

    def create(self, validated_data):
        user_obj = UserSede(**validated_data)
        user_obj.save()
        return user_obj

    def update(self, instance, validated_data):
        instance.user = validated_data["user"]
        instance.sede = validated_data["sede"]
        instance.save()
        return instance

class CampaignSerializer(serializers.ModelSerializer):
    """Serializer for Campaign model"""
    class Meta:
        model = Campaign
        
        fields = [
            'id', 'name', 'datetime_init', 'datetime_end',
            'daytime_init', 'daytime_end', 'retries',
            'trunk', 'context', 'queue',
            'max_canales', 'num_completadas', 'promedio',
            'desviacion', 'script', 'estatus', 'id_url'
        ]

    def create(self, validated_data):
        campaign_obj = Campaign(**validated_data)
        campaign_obj.save()
        return campaign_obj

    def update(self, instance, validated_data):
        instance.name = validated_data['name']
        instance.datetime_init = validated_data['datetime_init']
        instance.datetime_end = validated_data['datetime_end']
        instance.daytime_init = validated_data['daytime_init']
        instance.daytime_end = validated_data['daytime_end']
        instance.retries = validated_data['retries']
        instance.trunk = validated_data['trunk']
        instance.context = validated_data['context']
        instance.queue = validated_data['queue']
        instance.max_canales = validated_data['max_canales']
        instance.num_completadas = validated_data['num_completadas']
        instance.promedio = validated_data['promedio']
        instance.desviacion = validated_data['desviacion']
        instance.script = validated_data['script']
        instance.estatus = validated_data['estatus']
        instance.id_url = validated_data['id_url']
        instance.save()
        return instance

class CampaignEntrySerializer(serializers.ModelSerializer):
    """Serializer for campaign entry model"""
    class Meta:
        model = CampaignEntry
        fields = [
            'id',
            'name',
            'id_queue_call_entry',
            'id_form',
            'datetime_init',
            'datetime_end',
            'daytime_init',
            'daytime_end',
            'estatus',
            'script',
            'id_url',
        ]

    def create(self, validated_data):
        campaign_obj = CampaignEntry(**validated_data)
        campaign_obj.save()
        return campaign_obj

    def update(self, instance, validated_data):
        instance.name = validated_data['name']
        instance.id_queue_call_entry = validated_data['id_queue_call_entry']
        instance.id_form = validated_data['id_form']
        instance.datetime_init = validated_data['datetime_init']
        instance.datetime_end = validated_data['datetime_end']
        instance.daytime_init = validated_data['daytime_init']
        instance.daytime_end = validated_data['daytime_end']
        instance.estatus = validated_data['estatus']
        instance.script = validated_data['script']
        instance.id_url = validated_data['id_url']
        return instance

class CallsSerializer(serializers.ModelSerializer):
    """Serializer for calls model"""
    class Meta:
        model = Calls
        fields = [
            'id',
            'id_campaign',
            'phone',
            'status',
            'uniqueid',
            'fecha_llamada',
            'start_time',
            'end_time',
            'retries',
            'duration',
            'id_agent',
            'transfer',
            'datetime_entry_queue',
            'duration_wait',
            'dnc',
            'date_init',
            'date_end',
            'time_init',
            'time_end',
            'agent',
            'failure_cause',
            'failure_cause_txt',
            'datetime_originate',
            'trunk',
            'scheduled'
        ]

    def create(self, validated_data):
        calls_obj = Calls(**validated_data)
        calls_obj.save()
        return calls_obj

    def update(self, instance, validated_data):
        instance.id_campaign = validated_data['id_campaign']
        instance.phone = validated_data['phone']
        instance.status = validated_data['status']
        instance.uniqueid = validated_data['uniqueid']
        instance.fecha_llamada = validated_data['fecha_llamada']
        instance.start_time = validated_data['start_time']
        instance.end_time = validated_data['end_time']
        instance.retries = validated_data['retries']
        instance.duration = validated_data['duration']
        instance.id_agent = validated_data['id_agent']
        instance.transfer = validated_data['transfer']
        instance.datetime_entry_queue = validated_data['datetime_entry_queue']
        instance.duration_wait = validated_data['duration_wait']
        instance.dnc = validated_data['dnc']
        instance.date_init = validated_data['date_init']
        instance.date_end = validated_data['date_end']
        instance.time_init = validated_data['time_init']
        instance.time_end = validated_data['time_end']
        instance.agent = validated_data['agent']
        instance.failure_cause = validated_data['failure_cause']
        instance.failure_cause_txt = validated_data['failure_cause_txt']
        instance.datetime_originate = validated_data['datetime_originate']
        instance.trunk = validated_data['trunk']
        instance.scheduled = validated_data['scheduled']
        instance.save()
        return instance

class CallEntrySerializer(serializers.ModelSerializer):
    """Serializer for CrmCitas model"""
    class Meta:
        model = CallEntry
        fields = '__all__'

class CurrentCallEntrySerializer(serializers.ModelSerializer):
    """Serializer for CrmCitas model"""
    class Meta:
        model = CurrentCallEntry
        fields = [
            'id_agent',
            'id_queue_call_entry',
            'id_call_entry',
            'callerid',
            'datetime_init',
            'uniqueid',
            'channelclient',
            'hold',
        ]