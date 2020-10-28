"""Manages the agent state logic """
from datetime import datetime
import pytz
from django.db.models import Q
from dms.models import Terceros
from dms.serializers import TercerosSerializer
from consolidacion.models import CallConsolidacion
from campaigns.models import CampaignForm, AnswersHeader
from campaigns.serializers import DataLlamadaSerializar
from agent_console.models import (
    Audit, Agent, CurrentCallEntry,
    CedulaLlamada, ServerLog, CurrentCalls, AgentConsoleOptions)

class AgentState():
    """Class for agent state logic"""
    def __init__(self, verbosity=False):
        self.verbosity = verbosity

    @staticmethod
    def is_loged(id_agent):
        """ Checks if agent is loged to the call center module"""
        try:
            last_logon = Audit.objects.filter(
                id_agent=id_agent,
                id_break__isnull=True
            ).order_by('-datetime_init')[0]
            if last_logon.datetime_end == '' or last_logon.datetime_end is None:
                return True
            return False
        except IndexError:
            return False

    @staticmethod
    def agent_exist(id_agent):
        """Check if the agent still exist in the call_center db"""
        try:
            agent = Agent.objects.get(id=id_agent)
            return True, agent.number
        except Agent.DoesNotExist:
            return False, 0

    @staticmethod
    def agent_current_call_entry(id_agent):
        """Get the current call of the agent, None if there is no call"""
        try:
            query = CurrentCallEntry.objects.get(id_agent=id_agent)
            return query
        except CurrentCallEntry.DoesNotExist:
            return None

    @staticmethod
    def agent_current_call(agentnum):
        """Get the current call of the agent, None if there is no call"""
        try:
            query = CurrentCalls.objects.get(agentnum=agentnum)
            return query
        except CurrentCalls.DoesNotExist:
            return None

    @staticmethod
    def get_cedula(uniqueid):
        """Gets the document from the cedula_llamada table"""
        try:
            query = CedulaLlamada.objects.get(uniqueid=uniqueid)
            cedula = query.cedula
            return cedula
        except CedulaLlamada.DoesNotExist:
            return None

    @staticmethod
    def answer_borrado(answer):
        """Gets the answer for a delete agent scenario"""
        answer['message'] = "El agente fue borrado del servidor de telefonía"
        answer['call'] = False
        answer['status'] = "No encontrado"
        return answer

    @staticmethod
    def answer_not_logged(answer):
        """Gets the answer for a not agent logged scenario"""
        answer['message'] = "Por favor, inicie sesión en su telefono"
        answer['call'] = False
        answer['status'] = "No conectado"
        return answer

    @staticmethod
    def answer_call_wait(answer):
        """Gets the answer for a call wait scenario"""
        answer['message'] = "Esperando llamada"
        answer['call'] = False
        answer['status'] = "Conectado"
        return answer

    @staticmethod
    def answer_consolidacion(answer, current_call, id_agent):
        """Gets the answer for a call consolidacion scenario"""
        consolidacion, call_consolidacion_id = AgentState.get_consolidacion_by_call(
            current_call.id_call.id
        )
        try:
            tercero = Terceros.objects.get(nit=consolidacion.cedula)
        except Terceros.DoesNotExist:
            tercero = {'nombres':'Tercero eliminado de la bd'}

        agent = Agent.objects.get(id=id_agent)

        answer['cedula'] = consolidacion.cedula
        answer['placa'] = consolidacion.placa
        answer['nombre'] = tercero.nombres
        answer['sede'] = consolidacion.sede.id
        try:
            answer['asesor'] = consolidacion.sede.asesor.name
        except:
            answer['asesor'] = ""
        answer['motivo'] = consolidacion.motivo.id
        answer['extension'] = agent.number
        answer['llamada_id'] = current_call.uniqueid
        answer['call_consolidacion_id'] = call_consolidacion_id
        return answer

    @staticmethod
    def answer_poll_no_data(answer, telefono, poll_campaign):
        """Gets the answer for a call poll scenario"""
        data_terceros = Terceros.objects.filter(Q(telefono_1=telefono) | Q(telefono_2=telefono))
        terceros = TercerosSerializer(instance=data_terceros, many=True).data
        answer['terceros'] = terceros
        answer['data_llamada'] = None
        answer['form'] = poll_campaign.form.id
        return answer

    @staticmethod
    def answer_poll(answer, call, telefono, poll_campaign):
        try:
            header = AnswersHeader.objects.get(call_id=call.id)
            if header.data_llamada is not None:
                data_llamada = header.data_llamada
                serializer = DataLlamadaSerializar(data_llamada).initial_data
                answer['data_llamada'] = serializer
                answer['terceros'] = []
                answer['header'] = header.id
                answer['llamada_id'] = call.uniqueid
                return answer
        except AnswersHeader.DoesNotExist:
            pass
        return AgentState.answer_poll_no_data(answer, telefono, poll_campaign)

    @staticmethod
    def answer_entry(answer, current_call_entry):
        """Gets the answer for a call entry scenario"""
        ce = current_call_entry.id_call_entry
        campaign_isabel = ce.id_campaign
        campaign = AgentState.get_poll_campaign(campaign_isabel, 2)
        answer['campaign'] = campaign.id if campaign is not None else None
        cedula = AgentState.get_cedula(current_call_entry.uniqueid)
        tercero = None
        if cedula is not None:
            try:
                tercero_data = Terceros.objects.get(nit=cedula)
                tercero = TercerosSerializer(tercero_data).data
            except Terceros.DoesNotExist:
                pass

        answer['message'] = "En llamada"
        answer['call'] = True
        answer['status'] = "Conectado"
        answer['phone'] = current_call_entry.callerid
        answer['cedula'] = cedula
        answer['terceros'] = [tercero]
        answer['data_llamada'] = None
        answer['llamada_id'] = ce.uniqueid
        return answer

    def get_answer(self, state, id_agent, current_call_entry=None, current_call=None):
        """Returns the server answer given a state"""
        answer = {}
        answer['previous'] = state
        if state == "1":
            answer = AgentState.answer_borrado(answer)
        elif state == "2":
            answer = AgentState.answer_not_logged(answer)
        elif state == "3":
            answer = AgentState.answer_call_wait(answer)
        elif state == "4":
            answer = AgentState.answer_entry(answer, current_call_entry)
        elif state == "5":
            id_campaign = current_call.id_call.id_campaign
            campaign_cosolidacion = AgentConsoleOptions.objects.get(option='CAMPAIGN_CONSOLIDACION').value
            poll_campaign = AgentState.get_poll_campaign(id_campaign, 1)
            telefono = current_call.id_call.phone

            answer['message'] = "En llamada"
            answer['call'] = True
            answer['status'] = "Conectado"
            answer['phone'] = telefono
            answer['header'] = None


            if id_campaign.id == int(campaign_cosolidacion):
                answer = AgentState.answer_consolidacion(answer, current_call, id_agent)

            elif poll_campaign is not None:
                answer['campaign'] = poll_campaign.id
                answer['llamada_id'] = current_call.id_call.id
                answer['agente'] = id_agent
                answer = AgentState.answer_poll(answer, current_call.id_call, telefono, poll_campaign)
        if self.verbosity:
            self.save_log(state, id_agent, answer)
        answer['update'] = True
        return answer

    def save_log(self, state, id_agent, answer):
        """Saves a log with the agent state data"""
        timezone = pytz.timezone("America/Bogota")
        server_log = ServerLog(
            event=state,
            agent=id_agent,
            description=answer['message'],
            datetime=timezone.localize(datetime.now())
        )
        server_log.save()
        print("saved " + str(id_agent))

    @staticmethod
    def check_state(id_agent):
        """Gets the agent state based on the CurrentCallEntry and the 
        CurrentCall data"""
        current_call = None
        current_call_entry = None
        exist, agentnum = AgentState.agent_exist(id_agent)
        if not exist:
            state = "1"
        elif not AgentState.is_loged(id_agent):
            state = "2"
        else:
            current_call_entry = AgentState.agent_current_call_entry(id_agent)
            current_call = AgentState.agent_current_call(agentnum)
            if current_call_entry is None and current_call is None:
                state = "3"
            elif current_call_entry is not None:
                state = "4"
            else:
                state = "5"

        return state, current_call_entry, current_call

    @staticmethod
    def get_consolidacion_by_call(id_call):
        """Obtains a consolidacion based on call id"""
        consolidacion = CallConsolidacion.objects.get(call=id_call)
        return consolidacion.consolidacion, consolidacion.id

    @staticmethod
    def get_poll_campaign(id_campaign, type_campaign):
        """Checks if the given id matches a poll campaign"""
        try:
            campaign = CampaignForm.objects.get(
                isabel_campaign=id_campaign.id, 
                type_campaign=type_campaign
            )
        except CampaignForm.DoesNotExist:
            campaign = None
        return campaign
