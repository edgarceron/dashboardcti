import csv
from django.conf import settings
from campaigns.models import CampaignForm, AnswersBody, AnswersHeader, DataLlamada, Question

DATA_LLAMADA_HEADER = ['telefono', 'name', 'cedula', 'correo', 'placa', 'linea_veh']

def data_to_csv(collected_data):
    csvfile = open(settings.STATIC_ROOT + 'result.csv', 'w')
    writer = csv.writer(
        csvfile, delimiter=';', quotechar='|', quoting=csv.QUOTE_MINIMAL, lineterminator = '\n')
    for row in collected_data:
        writer.writerow(list(row.values()))
    return settings.STATIC_ROOT + 'result.csv'

def collect_data(id_campaign):
    campaign = CampaignForm.objects.get(id=id_campaign)
    headers = AnswersHeader.objects.filter(campaing=id_campaign)
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
    row = {}
    for data in DATA_LLAMADA_HEADER:
        row[data] = ""

    for question in questions:
        row[question.id] = ""
    return row

def multiple_answers(header, question, count=False):
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
