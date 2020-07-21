"""Contains the serializers for the motivos module"""
from rest_framework import serializers
from .models import Motivo

class MotivoSerializer(serializers.ModelSerializer):
    """Serializer for motivos model"""
    class Meta:
        model = Motivo
        fields = ['id', 'name', 'active']

    def create(self, validated_data):
        obj = Motivo(**validated_data)
        obj.save()
        return obj

    def update(self, instance, validated_data):
        instance.name = validated_data["name"]
        instance.active = validated_data["active"]
        instance.save()
        return instance
