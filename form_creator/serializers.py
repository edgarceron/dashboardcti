"""Contains the serializers for the form_creator module"""
from rest_framework import serializers
from .models import Form, Question, Answer

class FormSerializer(serializers.ModelSerializer):
    """Serializer for form model"""
    class Meta:
        model = Form
        fields = ['id', 'name']

    def create(self, validated_data):
        form_obj = Form(**validated_data)
        form_obj.save()
        return form_obj

    def update(self, instance, validated_data):
        instance.name = validated_data["name"]
        instance.save()
        return instance

class QuestionSerializer(serializers.ModelSerializer):
    """Serializer for Question model"""
    class Meta:
        model = Question
        fields = ['id', 'text', 'question_type', 'empty', 'form', 'position']

    def create(self, validated_data):
        question_obj = Question(**validated_data)
        question_obj.save()
        return question_obj

    def update(self, instance, validated_data):
        instance.text = validated_data["text"]
        instance.question_type = validated_data["question_type"]
        instance.empty = validated_data["empty"]
        instance.form = validated_data["form"]
        instance.position = validated_data["position"]
        instance.save()
        return instance

class AnswerSerializer(serializers.ModelSerializer):
    """Serializer for Answer model"""
    class Meta:
        model = Answer
        fields = ['id', 'question', 'text']

    def create(self, validated_data):
        question_obj = Answer(**validated_data)
        question_obj.save()
        return question_obj

    def update(self, instance, validated_data):
        instance.question = validated_data["question"]
        instance.text = validated_data["text"]
        instance.save()
        return instance
