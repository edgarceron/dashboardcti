"""Contains the serializers for the motivos module"""
from rest_framework import serializers
from consolidacion.business_logic.list_class import ConsolidacionList
from .models import Consolidacion, ConsolidacionFileUploads

class ConsolidacionSerializer(serializers.ModelSerializer):
    """Serializer for motivos model"""
    class Meta:
        model = Consolidacion
        fields = ['id', 'cedula', 'placa', 'fecha', 'motivo', 'sede']

    def create(self, validated_data):
        obj = Consolidacion(**validated_data)
        obj.save()
        return obj

    def update(self, instance, validated_data):
        instance.cedula = validated_data["cedula"]
        instance.placa = validated_data["placa"]
        instance.fecha = validated_data["fecha"]
        instance.motivo = validated_data["motivo"]
        instance.motivo = validated_data["sede"]
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
