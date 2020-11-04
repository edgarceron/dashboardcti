import csv, json
from datetime import timedelta, datetime
from django.conf import settings
from agent_console.models import Calls, CallEntry
from campaigns.models import CampaignForm, AnswersBody, AnswersHeader, DataLlamada, Question, Answer

DATA_LLAMADA_HEADER = ['telefono', 'name', 'cedula', 'correo', 'placa', 'linea_veh']
SALIENTE = 1
ENTRANTE = 2

def data_to_csv(collected_data):
    """Transforms the collected data into a csv file a return"""
    csvfile = open(settings.STATIC_ROOT + 'result.csv', 'w')
    writer = csv.writer(
        csvfile, delimiter=';', quotechar='|', quoting=csv.QUOTE_MINIMAL, lineterminator = '\n')
    for row in collected_data:
        writer.writerow(list(row.values()))
    return settings.STATIC_ROOT + 'result.csv'


def headers_date_range(start_date, end_date, campaign):
    """Get the answers headers which had a call in the given data range in the given
    campaign"""
    criteria = {}
    isabel_campaign = campaign.isabel_campaign
    type_campaign = campaign.type_campaign

    criteria['id_campaign'] = isabel_campaign
    if type_campaign == SALIENTE:
        if start_date != "" and end_date != "":
            start_date = datetime.strptime(end_date, '%Y-%m-%d')
            end_date = datetime.strptime(end_date, '%Y-%m-%d') + timedelta(seconds=86399)
            criteria['datetime_entry_queue__range'] = (start_date, end_date)

        elif start_date != "":
            start_date = datetime.strptime(end_date, '%Y-%m-%d')
            criteria['datetime_entry_queue__gte'] = start_date

        elif end_date != "":
            end_date = datetime.strptime(end_date, '%Y-%m-%d') + timedelta(seconds=86399)
            criteria['datetime_entry_queue__lte'] = end_date

        calls = list(Calls.objects.values_list('id', flat=True).filter(**criteria))
    else:
        if start_date != "" and end_date != "":
            start_date = datetime.strptime(end_date, '%Y-%m-%d')
            end_date = datetime.strptime(end_date, '%Y-%m-%d') + timedelta(seconds=86399)
            criteria['datetime_init__range'] = (start_date, end_date)

        elif start_date != "":
            start_date = datetime.strptime(end_date, '%Y-%m-%d')
            criteria['datetime_init__gte'] = start_date

        elif end_date != "":
            end_date = datetime.strptime(end_date, '%Y-%m-%d') + timedelta(seconds=86399)
            criteria['datetime_init__lte'] = end_date

        calls = list(CallEntry.objects.values_list('id', flat=True).filter(**criteria))

    headers = AnswersHeader.objects.filter(call_id__in=calls, campaign=campaign.id)
    return headers

def data_chart(id_campaign, start_date, end_date):
    """Returns the data to build a pie chart for the quesiton answers"""
    campaign = CampaignForm.objects.get(id=id_campaign)
    headers = headers_date_range(start_date, end_date, campaign)
    questions = Question.objects.filter(form=campaign.form)

    data = {}
    for question in questions:
        if question.question_type == 3 or question.question_type == 4:
            data[question.id] = {}
            data[question.id]['text'] = question.text

            answers = Answer.objects.filter(question=question.id)
            data_answers = {}

            for answer in answers:
                data_answers[answer.id] = {}
                data_answers[answer.id]['text'] = answer.text
                data_answers[answer.id]['count'] = 0

            data[question.id]['answers'] = data_answers

        if question.question_type == 1:
            data[question.id] = {}
            data[question.id]['text'] = question.text

            answers = Answer.objects.filter(question=question.id)
            data_answers = {}

            data_answers["true"] = {}
            data_answers["true"]['text'] = "Verdadero"
            data_answers["true"]['count'] = 0
            data_answers["false"] = {}
            data_answers["false"]['text'] = "Falso"
            data_answers["false"]['count'] = 0

            data[question.id]['answers'] = data_answers
    print(headers)
    for header in headers:
        bodies = AnswersBody.objects.filter(header=header.id)
        for body in bodies:
            if body.question.id in data:
                if body.question.question_type >= 3:
                    data[body.question.id]['answers'][body.answer.id]['count'] += 1
                else:
                    print("body.answer_text")
                    data[body.question.id]['answers'][str(body.answer_text)]['count'] += 1
    return json.dumps(data)


def collect_data(id_campaign, start_date="", end_date=""):
    """Gets the answers for the given campaign in the given data range including
    the data of the interviewee"""
    campaign = CampaignForm.objects.get(id=id_campaign)
    headers = headers_date_range(start_date, end_date, campaign)
    questions = Question.objects.filter(form=campaign.form)

    collected_data = []
    for header in headers:
        row = new_row(questions)
        data_llamada = DataLlamada.objects.get(id=header.data_llamada.id)

        row['telefono'] = data_llamada.telefono
        row['name'] = data_llamada.name
        row['cedula'] = data_llamada.cedula
        row['correo'] = data_llamada.correo
        row['placa'] = data_llamada.placa
        row['linea_veh'] = data_llamada.linea_veh

        bodies = AnswersBody.objects.filter(header=header.id)
        multiple_resolved = []
        for body in bodies:
            if body.question.id in multiple_resolved:
                continue

            if multiple_answers(header.id, body.question.id, True) > 1:
                answers = multiple_answers(header.id, body.question.id)
                multiple_resolved.append(body.question.id)
                result = ""
                for ans in answers:
                    result = result + ans.answer_text + "-"
            else:
                result = body.answer_text
            row[body.question.id] = result
        collected_data.append(row)
    return collected_data

def new_row(questions):
    """Creates an dictionary to hold interviewee data"""
    row = {}
    for data in DATA_LLAMADA_HEADER:
        row[data] = ""

    for question in questions:
        row[question.id] = ""
    return row

def multiple_answers(header, question, count=False):
    """Return multiple answers count or data for the given header and question"""
    answers = AnswersBody.objects.filter(header=header, question=question)
    if count:
        return len(answers)
    return answers

def delete_all():
    a = AnswersBody.objects.all()
    for x in a:
        x.delete()
    a = AnswersHeader.objects.all()
    for x in a:
        x.delete()
