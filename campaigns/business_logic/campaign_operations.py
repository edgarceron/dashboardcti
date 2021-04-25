"""Contains crud extra operations for campaigns app"""
import csv
from django.db.models import Q
from rest_framework import status
from rest_framework.response import Response
from users.permission_validation import PermissionValidation
from consolidacion.serializers import ConsolidacionFileUploadsSerializer
from agent_console.models import Calls, Campaign
from campaigns.serializers import DataLlamadaSerializar
from campaigns.models import CampaignForm, AnswersHeader, Question, AnswersBody, Answer, DataLlamada
from campaigns.business_logic import show_results, fail_management
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
            return error_outbound_campaign()
        del data['id']
        message = "Error al intentar guardar el archivo"
        file_serializer = ConsolidacionFileUploadsSerializer(data=data)
        if file_serializer.is_valid():
            file_serializer.save()
            file_name = file_serializer.data['file']
            fails = []
            with open(file_name, newline='', encoding='latin-1') as csvfile:
                spamreader = csv.reader(csvfile, delimiter=';', quotechar='|')
                line = 1
                for row in spamreader:
                    data = obtain_data_from_row(row)
                    data_llamada = DataLlamadaSerializar(data=data)
                    if data_llamada.is_valid():
                        campaign_isabel = campaign.isabel_campaign
                        call_id = create_call(data['telefono'], campaign_isabel)
                        if call_id is None:
                            message = "La campaña no esta asociada a una campaña en isabel"
                            return Response(
                                {"success":False, "message": message},
                                status=status.HTTP_400_BAD_REQUEST,
                                content_type='application/json'
                            )
                        model_data_llamada = data_llamada.save()
                        answer_header = create_answer_header(campaign, call_id, model_data_llamada)
                        answer_header.save()
                    else:
                        fails.append(';'.join(row))
                    line += 1
            return ok_response_upload(fails)
        return error_respose_upload()
    return permission_obj.error_response_webservice(validation, request)

def error_outbound_campaign():
    return Response(
        {
            "success":False, 
            "message": "No se pueden agragar datos para una campaña entrante"
        },
        status=status.HTTP_400_BAD_REQUEST,
        content_type='application/json'
    )

def get_campaign(id_campaign):
    try:
        campaign = CampaignForm.objects.get(id=id_campaign)
    except CampaignForm.DoesNotExist:
        campaign = None
    return campaign

def create_call(phone, id_campaign):
    try:
        campaign = Campaign.objects.get(id=id_campaign)
        campaign.estatus = 'A'
        campaign.save()
        call = Calls(phone=phone, id_campaign=campaign, retries=0, dnc=0, scheduled=0)
        call.save()
        return call.id
    except Campaign.DoesNotExist:
        return None

def create_answer_header(campaign, call_id, model_data_llamada):
    answer_header = AnswersHeader(
        campaign=campaign, tercero=None,
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
            if check_answers(answer_data) and question.question_type != 2:
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
        body = AnswersBody(header=header, question=question, question_text=question.text, 
        answer=None, answer_text="")
        body.save()
    else:
        for answer in answers:
            body = AnswersBody(header=header, question=question, question_text=question.text,
            answer=answer, answer_text=answer.text)
            body.save()

def store_answer_bool_text(answer, header, question):
    if isinstance(answer, bool):
        if answer:
            answer = "Verdadero"
        else:
            answer = "Falso"

    body = AnswersBody(
        header=header, question=question, question_text=question.text,
        answer=None, answer_text=answer)
    body.save()

def check_answers(data_answers):
    if isinstance(data_answers, bool): 
        return False
    if isinstance(data_answers, str):
        try:
            data = json.loads(data_answers)
            if isinstance(data, str):
                return False
            if isinstance(data, int):
                return True
            elif not isinstance(data, list):
                return False 
        except json.decoder.JSONDecodeError:
            return False
    return True

def data_chart(request):
    """Returns the data to create charts for every questions"""
    permission_obj = PermissionValidation(request)
    validation = permission_obj.validate('save_answers')
    if validation['status']:
        data = request.data
        id_campaign = data['id_campaign']
        start_date = data['start_date']
        end_date = data['end_date']
        result = show_results.data_chart(id_campaign, start_date, end_date)
        return Response(
            {"success":True, "questions": result},
            status=status.HTTP_200_OK,
            content_type='application/json'
        )
    return permission_obj.error_response_webservice(validation, request)

def fail_prepare_polls(request):
    """Create new consolidations for failed consolidations in a given date range"""
    permission_obj = PermissionValidation(request)
    validation = permission_obj.validate('fail_prepare_polls')
    if validation['status']:
        data = request.data
        try:
            fail_management.prepare_to_call(data['campaign'], data['start_date'], data['end_date'])
            success = True
            message = "Se volvera a llamar a las encuestas fallidas"
        except:
            success = False
            message = "Ocurrio un error al intentar crear las llamadas"
        return Response(
            {"success":success, "message": message},
            status=status.HTTP_400_BAD_REQUEST,
            content_type='application/json'
        )
    return permission_obj.error_response_webservice(validation, request)

def new_upload_calls_campaign(request):
    """Creates the data for making manual calls from a file"""
    permission_obj = PermissionValidation(request)
    validation = permission_obj.validate('new_upload_calls_campaign')
    if validation['status']:
        data = request.data.copy()
        id_campaign = data['id']
        campaign = get_campaign(id_campaign)
        if campaign.type_campaign == 2:
            return error_outbound_campaign()
        del data['id']
        
        file_serializer = ConsolidacionFileUploadsSerializer(data=data)
        if file_serializer.is_valid():
            file_serializer.save()
            file_name = file_serializer.data['file']
            fails = go_through_file(file_name, campaign)
            return ok_response_upload(fails)
        return error_respose_upload()
    return permission_obj.error_response_webservice(validation, request)

def go_through_file(file_name, campaign):
    fails = ""
    with open(file_name, newline='', encoding='latin-1') as csvfile:
        spamreader = csv.reader(csvfile, delimiter=';', quotechar='|')
        line = 1
        for row in spamreader:
            data = obtain_data_from_row(row)
            data_llamada = DataLlamadaSerializar(data=data)
            if data_llamada.is_valid():
                campaign_isabel = campaign.isabel_campaign
                model_data_llamada = data_llamada.save()
                answer_header = create_answer_header(campaign, None, model_data_llamada)
                answer_header.save()
            else:
                fails.append(';'.join(row))
            line += 1
    return fails

def ok_response_upload(fails):
    return Response(
        {
            "success":True,
            "message": "Archivo subido correctamente",
            "fails": fails
        },
        status=status.HTTP_201_CREATED,
        content_type='application/json'
    )

def error_respose_upload():
    message = "Error al intentar guardar el archivo"
    return Response(
        {"success":False, "message": message},
        status=status.HTTP_400_BAD_REQUEST,
        content_type='application/json'
    )

def detect_peding_calls(campaign):
    isabel_campaign = Campaign.objects.get(pk=campaign.isabel_campaign)
    retries = isabel_campaign.retries
    pending_calls = Calls.objects.filter(id_campaign=isabel_campaign.id, Q(retries_lt=retries) | Q(status="Placing") )
    return pending_calls

def process_more_calls(request):
    validation = permission_obj.validate('process_more_calls')
    if validation['status']:
        data = request.data
        id_campaign = data['id_campaign']
        simmultaneous = data['simmultaneous']
        campaign = CampaignForm.objects.get(pk=id_campaign)
        putted, pending_headers = put_more_calls(campaign, simmultaneous)
        return Response(
            {
                "success":True,
                "fails": putted,
                "pending_headers": pending_headers - putted
            },
            status=status.HTTP_200_OK,
            content_type='application/json'
        )
    return permission_obj.error_response_webservice(validation, request)

def put_more_calls(campaign, simmultaneous):
    isabel_campaign = Campaign.objects.get(pk=campaign.isabel_campaign)
    pending_calls = detect_peding_calls(campaign)
    calls_to_put = simmultaneous - pedingcalls.count()
    headers = AnswersHeader.objects.filter(campaign=campaign.id, call_id=None)
    pending_headers = headers.count()
    putted = 0
    for header in headers:
        if calls_to_put > 0:
            phone = get_phone(header.data_llamada)
            create_call(phone, isabel_campaign)
            calls_to_put-=1
            putted+=1
        else:
            break
    return putted, pending_headers


def get_phone(data_llamada_id):
    try:
        data_llamada = DataLlamada.objects.get(pk=data_llamada_id)
        return data_llamada.telefono
    except DataLlamada.DoesNotExist:
        return None