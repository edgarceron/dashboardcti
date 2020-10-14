from rest_framework import serializers
from .models import CampaignForm, AnswersHeader, AnswersBody

class CampaignFormSerializer(serializers.ModelSerializer):
    """Serializer for CampaingForm model"""
    class Meta:
        model = CampaignForm
        fields = ['id', 'type_campaign', 'isabel_campaign', 'form']

    def create(self, validated_data):
        obj = CampaignForm(**validated_data)
        obj.save()
        return obj

    def update(self, instance, validated_data):
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
