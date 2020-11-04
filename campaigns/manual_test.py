import names, string, time
from random import randint, choice, random
from agent_console.models import CallEntry, Calls, Agent, Campaign, QueueCallEntry, CampaignEntry
from campaigns.business_logic import show_results
from campaigns.models import CampaignForm, AnswersBody, AnswersHeader, Answer, Question, DataLlamada


def test(n):
    campaign = CampaignForm.objects.get(id=1)
    campaign_entry = CampaignForm.objects.get(id=2)
    isabel_campaign = Campaign.objects.get(id=campaign.isabel_campaign)
    isabel_campaign_entry = CampaignEntry.objects.get(id=campaign_entry.isabel_campaign)

    calls = create_calls(n, isabel_campaign)
    data_llamadas = create_data_llamadas(n)
    headers = create_headers(campaign, calls, data_llamadas)
    bodies = create_bodies(campaign.form, headers)

    call_entry = create_call_entry(n, isabel_campaign_entry)
    data_llamadas_entry = create_data_llamadas(n)
    headers_entry = create_headers(campaign_entry, call_entry, data_llamadas_entry)
    bodies_entry = create_bodies(campaign_entry.form, headers_entry)

    return calls, data_llamadas, headers, bodies, call_entry, data_llamadas_entry, headers_entry, bodies_entry

def create_calls(n, campaign):
    calls = []
    for i in range(n):
        calls.append(
            Calls(
                id_campaign=campaign,
                phone=randint(1000000000, 9999999999),
                datetime_entry_queue=random_date(
                    "2020-11-03 08:00:00",
                    "2020-11-03 20:00:00",
                    random()
                ),
                status="Success",
                agent=Agent.objects.get(pk=ramdom_agent()),
                retries=0,
                dnc=0,
                scheduled=0
            )
        )
    for i in range(n):
        calls[i].save()
    return calls

def create_call_entry(n, campaign):
    calls = []
    for i in range(n):
        calls.append(
            CallEntry(
                id_campaign=campaign,
                trunk="aaaa",
                id_queue_call_entry=QueueCallEntry.objects.get(id=1),
                callerid=randint(1000000000, 9999999999),
                datetime_entry_queue=random_date(
                    "2020-11-03 08:00:00",
                    "2020-11-03 20:00:00",
                    random()
                ),
                status="terminada",
                id_agent=Agent.objects.get(pk=ramdom_agent())
            )
        )
    for i in range(n):
        calls[i].save()
    return calls

def create_data_llamadas(n):
    data_llamadas = []
    for i in range(n):
        data_llamadas.append(DataLlamada(
            name=names.get_full_name(),
            telefono=str(randint(1000000000, 9999999999)),
            cedula=str(randint(1000000000, 9999999999)),
            correo=names.get_first_name() + "@gmail.com",
            placa=get_random_string(3) + str(randint(100, 999)),
            linea_veh=names.get_last_name()
        ))
    for i in range(n):
        data_llamadas[i].save()
    return data_llamadas

def create_headers(campaign, calls, data_llamadas):
    headers = []
    while calls != []:
        data_llamada=data_llamadas.pop(0)
        call = calls.pop(0)
        headers.append(AnswersHeader(
            campaign=campaign,
            tercero=None,
            agente=ramdom_agent(),
            call_id=call.id,
            data_llamada=data_llamada
        ))
    for i in range(len(headers)):
        headers[i].save()
    return headers

def create_bodies(form, headers):
    questions = Question.objects.filter(form=form)
    bodies = []

    for header in headers:
        for question in questions:
            if question.question_type == 3 or question.question_type == 4:
                answers = Answer.objects.filter(question=question.id)
                answer = choice(answers)
                bodies.append(AnswersBody(
                    header=header,
                    question=question,
                    question_text=question.text,
                    answer=answer,
                    answer_text=answer.text
                ))
            else:
                bodies.append(AnswersBody(
                    header=header,
                    question=question,
                    question_text=question.text,
                    answer=None,
                    answer_text="F"
                ))
    for i in range(len(bodies)):
        bodies[i].save()
    return bodies

def ramdom_agent():
    agentes = [1, 2, 3, 6, 7, 8, 9, 10]
    selected = randint(0, len(agentes)-1)
    return agentes[selected]

def delete_models(models):
    for x in models:
        x.delete()

def delete_all():
    baodies = AnswersBody.objects.all()
    headers = AnswersHeader.objects.all()
    delete_models(baodies)
    delete_models(headers)

def get_random_string(length):
    letters = string.ascii_lowercase
    result_str = ''.join(choice(letters) for i in range(length))
    return result_str

def str_time_prop(start, end, format, prop):
    """Get a time at a proportion of a range of two formatted times.

    start and end should be strings specifying times formated in the
    given format (strftime-style), giving an interval [start, end].
    prop specifies how a proportion of the interval to be taken after
    start.  The returned time will be in the specified format.
    """

    stime = time.mktime(time.strptime(start, format))
    etime = time.mktime(time.strptime(end, format))

    ptime = stime + prop * (etime - stime)

    return time.strftime(format, time.localtime(ptime))

def random_date(start, end, prop):
    return str_time_prop(start, end, '%Y-%m-%d %H:%M:%S', prop)
