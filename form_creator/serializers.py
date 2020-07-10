"""Contains the serializers for the form_creator module"""
from rest_framework import serializers
from .models import Form

class FormSerializer(serializers.ModelSerializer):
    """Serializer for form model"""
    class Meta:
        model = Form
        fields = ['id', 'name']

    def create(self, validated_data):
        user_obj = User(**validated_data)
        user_obj.save()
        return user_obj

    def update(self, instance, validated_data):
        instance.name = validated_data["name"]
        instance.save()
        return instance