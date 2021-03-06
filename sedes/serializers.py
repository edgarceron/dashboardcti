"""Contains the serializers for the sedes module"""
from rest_framework import serializers
from dms.models import Bodegas
from .models import Sede

class SedeSerializer(serializers.ModelSerializer):
    """Serializer for motivos model"""
    class Meta:
        model = Sede
        fields = ['id', 'name', 'address', 'active', 'bodega_dms']

    def create(self, validated_data):
        obj = Sede(**validated_data)
        obj.save()
        return obj

    def update(self, instance, validated_data):
        instance.name = validated_data["name"]
        instance.address = validated_data["address"]
        instance.bodega_dms = validated_data["bodega_dms"]
        instance.active = validated_data["active"]
        instance.save()
        return instance

class BodegasSerializer(serializers.ModelSerializer):
    """Serializer for Bodegas model"""
    id = serializers.IntegerField(source='bodega')
    name = serializers.CharField(source='descripcion')

    class Meta:
        model = Bodegas
        fields = ['id', 'name']
