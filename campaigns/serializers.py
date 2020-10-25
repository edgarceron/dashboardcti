from rest_framework import serializers
from .models import CampaignForm, AnswersHeader, AnswersBody, DataLlamada

class CampaignFormSerializer(serializers.ModelSerializer):
    """Serializer for CampaingForm model"""
    
    class Meta:
        model = CampaignForm
        fields = ['id', 'name', 'type_campaign', 'isabel_campaign', 'form']

    def create(self, validated_data):
        obj = CampaignForm(**validated_data)
        obj.save()
        return obj

    def update(self, instance, validated_data):
        instance.name = validated_data["name"]
        instance.type_campaign = validated_data["type_campaign"]
        instance.isabel_campaign = validated_data["isabel_campaign"]
        instance.form = validated_data["form"]
        instance.save()
        return instance

class AnswersHeaderSerializer(serializers.ModelSerializer):
    """Serializer for AnswersHeader model"""
    class Meta:
        model = AnswersHeader
        fields = ['id', 'campaing', 'tercero']

    def create(self, validated_data):
        obj = AnswersHeader(**validated_data)
        obj.save()
        return obj

    def update(self, instance, validated_data):
        instance.campaing = validated_data["campaing"]
        instance.tercero = validated_data["tercero"]
        instance.save()
        return instance

class AnswersBodySerializer(serializers.ModelSerializer):
    """Serializer for AnswersBody model"""
    class Meta:
        model = AnswersBody
        fields = ['id', 'header', 'question', 'question_text', 'answer', 'answer_text']

    def create(self, validated_data):
        obj = AnswersBody(**validated_data)
        obj.save()
        return obj

    def update(self, instance, validated_data):
        instance.header = validated_data["header"]
        instance.question = validated_data["question"]
        instance.question_text = validated_data["question_text"]
        instance.answer = validated_data["answer"]
        instance.answer_text = validated_data["answer_text"]
        instance.save()
        return instance

class DataLlamadaSerializar(serializers.ModelSerializer):
    """Serializer for DataLlamada model"""
    class Meta:
        model = DataLlamada
        fields = [
            'id',
            'telefono',
            'name',
            'cedula',
            'correo',
            'placa',
            'linea_veh',
        ]

    def create(self, validated_data):
        obj = DataLlamada(**validated_data)
        obj.save()
        return obj

    def update(self, instance, validated_data):
        instance.telefono = validated_data["telefono"]
        instance.name = validated_data["name"]
        instance.cedula = validated_data["cedula"]
        instance.correo = validated_data["correo"]
        instance.placa = validated_data["placa"]
        instance.linea_veh = validated_data["linea_veh"]
        instance.save()
        return instance
