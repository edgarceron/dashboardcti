"""Contains crud extra operations for campaings app"""
import csv
from rest_framework import status
from rest_framework.response import Response
from users.permission_validation import PermissionValidation
from consolidacion.serializers import ConsolidacionFileUploadsSerializer
from agent_console.models import Calls, Campaign
from campaigns.serializers import DataLlamadaSerializar, AnswersBodySerializer
from campaigns.models import CampaignForm, AnswersHeader, Question, AnswersBody, Answer
import json

def upload_calls_campaign(request):
    """Uploads the calls for the campaign"""
    permission_obj = PermissionValidation(request)
    validation = permission_obj.validate('upload_consolidacion')
    if validation['status']:
        data = request.data.copy()
        id_campaign = data['id']
        campaign = get_campaign(id_campaign)
        if campaign.type_campaign == 2:
            return Response(
                {"success":False, "message": "No se pueden agragar datosp para una campaña entrante"},
                status=status.HTTP_400_BAD_REQUEST,
                content_type='application/json'
            )
        del data['id']
        file_serializer = ConsolidacionFileUploadsSerializer(data=data)
        if file_serializer.is_valid():
            file_serializer.save()
            file_name = file_serializer.data['file']
            fails = []
            with open(file_name, newline='') as csvfile:
                spamreader = csv.reader(csvfile, delimiter=';', quotechar='|')
                line = 1
                for row in spamreader:
                    data = obtain_data_from_row(row)
                    data_llamada = DataLlamadaSerializar(data=data)
                    if data_llamada.is_valid():
                        campaign_isabel = campaign.isabel_campaign
                        call_id = create_call(data['telefono'], campaign_isabel)
                        model_data_llamada = data_llamada.save()
                        answer_header = create_answer_header(campaign, call_id, model_data_llamada)
                        answer_header.save()
                    else:
                        fails.append(';'.join(row))
                    line += 1
            return Response(
                {
                    "success":True,
                    "message": "Archivo subido correctamente",
                    "fails": fails
                },
                status=status.HTTP_201_CREATED,
                content_type='application/json'
            )
        return Response(
            {"success":False, "message": "Error al intentar guardar el archivo"},
            status=status.HTTP_400_BAD_REQUEST,
            content_type='application/json'
        )
    return permission_obj.error_response_webservice(validation, request)

def get_campaign(id_campaign):
    try:
        campaign = CampaignForm.objects.get(id=id_campaign)
    except CampaignForm.DoesNotExist:
        campaign = None
    return campaign

def create_call(phone, id_campaign):
    campaign = Campaign.objects.get(id=id_campaign)
    campaign.estatus = 'A'
    campaign.save()
    call = Calls(phone=phone, id_campaign=campaign, retries=0, dnc=0, scheduled=0)
    call.save()
    return call.id

def create_answer_header(campaign, call_id, model_data_llamada):
    answer_header = AnswersHeader(
        campaing=campaign, tercero=None,
        agente=None, call_id=call_id,
        data_llamada=model_data_llamada
    )
    answer_header.save()
    return answer_header

def obtain_data_from_row(row):
    aux = 1
    data = {}
    for col in row:
        if aux == 1:
            data['cedula'] = col
        if aux == 2:
            data['name'] = col
        if aux == 3:
            data['correo'] = col
        if aux == 4:
            data['placa'] = col
        if aux == 5:
            data['telefono'] = col
        if aux == 6:
            data['linea_veh'] = col
        aux += 1
    return data

def save_answers(request, header_id):
    permission_obj = PermissionValidation(request)
    validation = permission_obj.validate('save_answers')
    if validation['status']:
        data = request.data
        keys = data.keys()
        header = AnswersHeader.objects.get(id=header_id)
        for question_id in keys:
            question = Question.objects.get(id=question_id)
            answer_data = data[question_id]
            if check_answers(answer_data):
                answers = obtain_asnwers(answer_data)
                store_answers(answers, header, question)
            else:
                store_answer_bool_text(answer_data, header, question)
        return Response(
            {"success":True, "message": "Respuestas guardadas correctamente"},
            status=status.HTTP_200_OK,
            content_type='application/json'
        )
    return permission_obj.error_response_webservice(validation, request)

def obtain_asnwers(data_answers):
    if isinstance(data_answers, str):
        data_answers = json.loads(data_answers)
    if isinstance(data_answers, list):
        answers = []
        for answer in data_answers:
            answers.append(Answer.objects.get(id=answer))
    else:
        answers = [Answer.objects.get(id=data_answers)]
    return answers

def store_answers(answers, header, question):
    if len(answers) == 0:
        body = AnswersBody(header, question, question.text, None, "")
        body.save()
    else:
        for answer in answers:
            body = AnswersBody(header=header, question=question, question_text=question.text,
            answer=answer, answer_text=answer.text)
            body.save()

def store_answer_bool_text(answer, header, question):
    if isinstance(answer, bool):
        if(answer):
            answer = "Verdadero"
        else:
            answer = "Falso"

    body = AnswersBody(header=header, question=question, question_text=question.text,
    answer=None, answer_text=answer)
    body.save()

def check_answers(data_answers):
    if isinstance(data_answers, bool): 
        return False
    if isinstance(data_answers, str):
        try:
            data = json.loads(data_answers)
            if not isinstance(data, list):
                return False 
        except json.decoder.JSONDecodeError:
            return False
    return True
