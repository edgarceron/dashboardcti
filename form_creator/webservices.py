"""Contains the webservices for the form_creator app"""
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework import status
from core.crud.standard import Crud
from users.permission_validation import PermissionValidation
from form_creator.business_logic import data_filters
from .models import Form, Question, Answer
from .serializers import FormSerializer, QuestionSerializer, AnswerSerializer

def get_actions():
    "Returns the list of actions to be registered for permissions module."
    actions = [
        {"name": "add_form", "label": "Webservice crear formulario"},
        {"name": "replace_form", "label": "Webservice actualizar formulario"},
        {"name": "get_form", "label": "Webservice obtener datos formulario"},
        {"name": "delete_form", "label": "Webservice borrar formulario"},
        {"name": "picker_search_form", "label": "Webservice picker de formularios"},
        {"name": "list_form", "label": "Webservice del listado de formularios"},
        {"name": "toggle_form", "label": "Webservice para cambiar estado del formulario"},
        {"name": "add_question", "label": "Webservice crear pregunta"},
        {"name": "replace_question", "label": "Webservice actualizar pregunta"},
        {"name": "delete_question", "label": "Webservice borrar pregunta"},
        {"name": "change_question_position", "label": "Webservice cambiar posición de la pregunta"},
        {"name": "add_answer", "label": "Webservice crear respuesta"},
        {"name": "replace_answer", "label": "Webservice actualizar respuesta"},
        {"name": "delete_answer", "label": "Webservice borrar respuesta"}
    ]
    return actions

@api_view(['POST'])
def add_form(request):
    """Tries to create a form and returns the result"""
    crud_object = Crud(FormSerializer, Form)
    return crud_object.add(request, 'add_form')

@api_view(['PUT'])
def replace_form(request, form_id):
    "Tries to update a form and returns the result"
    crud_object = Crud(FormSerializer, Form)
    return crud_object.replace(request, form_id, 'replace_form')

@api_view(['POST'])
def get_form(request, form_id):
    "Return a JSON response with form data for the given id"
    crud_object = Crud(FormSerializer, Form)
    return crud_object.get(request, form_id, 'get_form')

@api_view(['DELETE'])
def delete_form(request, form_id):
    """Tries to delete an form and returns the result."""
    crud_object = Crud(FormSerializer, Form)
    return crud_object.delete(request, form_id, 'delete_form', "Formulario elminado exitosamente")

@api_view(['POST'])
def toggle_form(request, form_id):
    """Toogles the active state for a given user"""
    crud_object = Crud(FormSerializer, Form)
    return crud_object.toggle(request, form_id, 'toggle_form', "Formulario")

@api_view(['POST'])
def picker_search_form(request):
    "Returns a JSON response with form data for a selectpicker."
    crud_object = Crud(FormSerializer, Form, data_filters.form_picker_filter)
    return crud_object.picker_search(request, 'picker_search_user')

@api_view(['POST'])
def list_form(request):
    """Returns a JSON response containing registered form for a datatable"""
    crud_object = Crud(FormSerializer, Form, data_filters.form_listing_filter)
    return crud_object.listing(request, 'list_form')

@api_view(['POST'])
def add_question(request):
    """Tries to create a question and returns the result"""
    crud_object = Crud(QuestionSerializer, Question)
    return crud_object.add(request, 'add_question')

@api_view(['PUT'])
def replace_question(request, question_id):
    """Tries to update a question and returns the result"""
    crud_object = Crud(QuestionSerializer, Question)
    return crud_object.replace(request, question_id, 'replace_question')

@api_view(['DELETE'])
def delete_question(request, question_id):
    """Tries to delete an question and returns the result."""
    crud_object = Crud(QuestionSerializer, Question)
    return crud_object.delete(request, question_id, 'delete_question', "Pregunta elminada exitosamente")

@api_view(['POST'])
def change_question_position(request):
    pass 

@api_view(['POST'])
def add_answer(request):
    """Tries to create a answer and returns the result"""
    crud_object = Crud(AnswerSerializer, Answer)
    return crud_object.add(request, 'add_answer')

@api_view(['PUT'])
def replace_answer(request, answer_id):
    """Tries to update a answer and returns the result"""
    crud_object = Crud(AnswerSerializer, Answer)
    return crud_object.replace(request, answer_id, 'replace_answer')

@api_view(['POST'])
def delete_answer(request, answer_id):
    """Tries to delete an answer and returns the result."""
    crud_object = Crud(AnswerSerializer, Answer)
    return crud_object.delete(request, answer_id, 'delete_answer', "Pregunta elminada exitosamente")
