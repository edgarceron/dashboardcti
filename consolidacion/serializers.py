"""Contains the serializers for the motivos module"""
from rest_framework import serializers
from consolidacion.business_logic.list_class import ConsolidacionList
from .models import Consolidacion, ConsolidacionFileUploads, CallConsolidacion

class ConsolidacionSerializer(serializers.ModelSerializer):
    """Serializer for consolidacion model"""
    class Meta:
        model = Consolidacion
        fields = ['id', 'cedula', 'placa', 'fecha', 'motivo', 'sede', 'observaciones']

    def create(self, validated_data):
        obj = Consolidacion(**validated_data)
        obj.save()
        return obj

    def update(self, instance, validated_data):
        instance.cedula = validated_data["cedula"]
        instance.placa = validated_data["placa"]
        instance.fecha = validated_data["fecha"]
        instance.motivo = validated_data["motivo"]
        instance.sede = validated_data["sede"]
        instance.save()
        return instance

class ConsolidacionListSerializer(serializers.Serializer):
    """Serializer for consolidacion listing format"""
    id = serializers.IntegerField()
    cedula = serializers.CharField(max_length=20)
    placa = serializers.CharField(max_length=10)
    fecha = serializers.DateField()
    motivo = serializers.CharField(max_length=50)
    sede = serializers.CharField(max_length=50)
    motivo_id = serializers.IntegerField()
    sede_id = serializers.IntegerField()

class ConsolidacionFileUploadsSerializer(serializers.ModelSerializer):
    class Meta:
        model = ConsolidacionFileUploads
        fields = ['file']

    def save(self, *args, **kwargs):
        if self.instance is not None and self.instance.file is not None:
            self.instance.file.delete()
        return super().save(*args, **kwargs)

class CallConsolidacionSerializer(serializers.ModelSerializer):
    """Serializer for CallConsolidacion model"""
    class Meta:
        model = CallConsolidacion
        fields = ['consolidacion', 'call', 'cita_tall_id', 'cita_crm_id', 'call_made']

    def create(self, validated_data):
        obj = CallConsolidacion(**validated_data)
        obj.save()
        return obj

    def update(self, instance, validated_data):
        instance.consolidacion = validated_data["consolidacion"]
        instance.call = validated_data["call"]
        instance.agent = validated_data["agent"]
        instance.cita_tall_id = validated_data["cita_tall_id"]
        instance.cita_crm_id = validated_data["cita_crm_id"]
        instance.save()
        return instance
