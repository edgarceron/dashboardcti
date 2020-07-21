"""Contains the serializers for the users module"""
from rest_framework import serializers
from .models import UserAgent, Agent, UserSede

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
