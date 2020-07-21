"""Contains the serializers for the motivos module"""
from rest_framework import serializers
from .models import Asesor

class AsesorSerializer(serializers.ModelSerializer):
    """Serializer for motivos model"""
    class Meta:
        model = Asesor
        fields = ['id', 'name', 'active', 'sede']

    def create(self, validated_data):
        obj = Asesor(**validated_data)
        obj.save()
        return obj

    def update(self, instance, validated_data):
        instance.name = validated_data["name"]
        instance.active = validated_data["active"]
        instance.sede = validated_data["sede"]
        instance.save()
        return instance
