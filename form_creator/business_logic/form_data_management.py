"""Manages webservices for questions and answers data in the form_creator app"""
import json 
from rest_framework import status
from rest_framework.response import Response
from users.permission_validation import PermissionValidation
from core.crud.standard import Crud
from form_creator.models import Question, Answer, Form
from form_creator.serializers import QuestionSerializer, AnswerSerializer, FormSerializer

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
            answers_by_question = {}
            for x in answers:
                x = dict(x)
                question = x["question"]
                if question in answers_by_question:
                    answers_by_question[question].append(x)
                else:
                    answers_by_question[question] = [x]

            data = {
                "success": True,
                "questions": questions,
                "answers": answers_by_question,
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

def save_all(request):
    """Saves form, questions and answers"""
    permission_obj = PermissionValidation(request)
    validation = permission_obj.validate("save_all")
    if validation['status']:
        data = request.data

        form_id = data['id']
        form_data = json.loads(data['form'])
        questions_data = json.loads(data['questions'])
        question_list = []
        for i in questions_data:
            question_data = json.loads(i)
            if "id" in question_data:
                update_question(question_data)
            else:
                question_list.append(question_data)

        answers_data = json.loads(data['answers'])

        answer_list = []
        for i in answers_data:
            answer_data = json.loads(i)
            if "id" in answer_data:
                update_answer(answer_data)
            else:
                answer_list.append(json.loads(i))

        save_form(form_data, form_id)
        save_questions(question_list)
        save_answers(answer_list)

        data = {
            "success": True
        }
        return Response(data, status=status.HTTP_200_OK, content_type='application/json')
    return permission_obj.error_response_webservice(validation, request)

def save_form(form_data, form_id=0):
    """Saves a form, used in save_all"""
    crud_object = Crud(FormSerializer, Form)
    answer, status = crud_object.save_instance(form_data, None, form_id)
    return answer

def save_questions(questions):
    """Save all questions of a form, used in save_all"""
    serializer = QuestionSerializer(data=questions, many=True)
    if serializer.is_valid():
        serializer.save()

def save_answers(answers):
    """Save all answers of a form, used in save_all"""
    serializer = AnswerSerializer(data=answers, many=True)
    if serializer.is_valid():
        serializer.save()

def update_question(data):
    """Updates a question individually"""
    id_question = data["id"]
    del data["id"]
    question = Question.objects.get(pk=id_question)
    serializer = QuestionSerializer(question, data=data)
    if serializer.is_valid():
        serializer.save()

def update_answer(data):
    """Updates a answer individually"""
    id_answer = data["id"]
    del data["id"]
    answer = Answer.objects.get(pk=id_answer)
    serializer = AnswerSerializer(answer, data=data)
    if serializer.is_valid():
        serializer.save()