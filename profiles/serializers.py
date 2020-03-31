from rest_framework import serializers
from .models import Profile, App, Action

class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model  = Profile
        fields = ['name']

    def create(self, validated_data):
        profile_obj     = Profile(**validated_data)
        profile_obj.save()
        return profile_obj

    def update(self, instance, validated_data):
        instance.name       = validated_data["name"]
        instance.save()
        return instance
    
class AppSerializer(serializers.ModelSerializer):
    class Meta:
        model  = App
        fields = ['name']

    def create(self, validated_data):
        app_obj     = App(**validated_data)
        app_obj.save()
        return app_obj

    def update(self, instance, validated_data):
        instance.name       = validated_data["name"]
        instance.save()
        return instance

class ActionSerializer(serializers.ModelSerializer):
    class Meta:
        model  = Action
        fields = ['name', 'app', 'label']

    def create(self, validated_data):
        action_obj     = Action(**validated_data)
        action_obj.save()
        return action_obj

    def update(self, instance, validated_data):
        instance.name       = validated_data["name"]
        instance.app        = validated_data["app"]
        instance.save()
        return instance