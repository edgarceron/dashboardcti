"""Manages webservices for questions and answers data in the form_creator app"""
from rest_framework import status
from rest_framework.response import Response
from users.permission_validation import PermissionValidation
from form_creator.models import Question, Answer
from form_creator.serializers import QuestionSerializer, AnswerSerializer

def get_questions_form(request, id_form):
    """Returns a json rensponse with the questions for the given form"""
    permission_obj = PermissionValidation(request)
    validation = permission_obj.validate("get_questions_form")
    if validation['status']:
        try:
            query = Question.objects.filter(form=id_form).order_by('position')
            serializer = QuestionSerializer(query, many=True)
            questions = serializer.data
            answers = get_answers_form(query)

            data = {
                "success": True,
                "questions": questions,
                "answers": answers,
            }
            return Response(data, status=status.HTTP_200_OK, content_type='application/json')
        except Question.DoesNotExist:
            data = {
                "success": False,
                "message": "No se encontro el formulario, quiza fue borrado antes de esta transacción"
            }
            return Response(data, status=status.HTTP_404_NOT_FOUND, content_type='application/json')
    return permission_obj.error_response_webservice(validation, request)

def get_answers_form(questions):
    """Returns the anwers for the given questions"""
    query = Answer.objects.filter(question__in=questions)
    serializer = AnswerSerializer(query, many=True)
    return serializer.data
