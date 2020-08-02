"""Manages the agent state logic """
from datetime import datetime
import pytz
from dms.models import Terceros
from consolidacion.models import CallConsolidacion
from agent_console.models import (
    Audit, Agent, CurrentCallEntry,
    CedulaLlamada, ServerLog, CurrentCalls)

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

    def get_answer(self, state, id_agent, current_call_entry=None, current_call=None):
        """Returns the server answer given a state"""
        answer = {}
        answer['previous'] = state
        if state == "1":
            answer['message'] = "El agente fue borrado del servidor de telefonía"
            answer['call'] = False
            answer['status'] = "No encontrado"

        elif state == "2":
            answer['message'] = "Por favor, inicie sesión en su telefono"
            answer['call'] = False
            answer['status'] = "No conectado"

        elif state == "3":
            answer['message'] = "Esperando llamada"
            answer['call'] = False
            answer['status'] = "Conectado"

        elif state == "4":
            agent = Agent.objects.get(id=id_agent)
            answer['message'] = "En llamada"
            answer['call'] = True
            answer['status'] = "Conectado"
            answer['phone'] = current_call_entry.callerid
            answer['cedula'] = AgentState.get_cedula(current_call_entry.uniqueid)
            answer['extension'] = agent.number
            answer['llamada_id'] = current_call_entry.uniqueid

        elif state == "5":
            consolidacion = AgentState.get_consolidacion_by_call(current_call.id_call.id)
            try:
                tercero = Terceros.objects.get(nit=consolidacion.cedula)
            except Terceros.DoesNotExist:
                tercero = {'nombres':'Tercero eliminado de la bd'}
            agent = Agent.objects.get(id=id_agent)
            answer['message'] = "En llamada"
            answer['call'] = True
            answer['status'] = "Conectado"
            answer['phone'] = current_call.id_call.phone
            answer['cedula'] = consolidacion.cedula
            answer['placa'] = consolidacion.placa
            answer['nombre'] = tercero.nombres
            answer['sede'] = consolidacion.sede.id
            answer['motivo'] = consolidacion.motivo.id
            answer['extension'] = agent.number
            answer['llamada_id'] = current_call.uniqueid

        if self.verbosity:
            timezone = pytz.timezone("America/Bogota")
            server_log = ServerLog(
                event=state,
                agent=id_agent,
                description=answer['message'],
                datetime=timezone.localize(datetime.now())
            )
            server_log.save()
            print("saved " + str(id_agent))
        answer['update'] = True
        return answer

    @staticmethod
    def check_state(id_agent):
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
        consolidacion = CallConsolidacion.objects.get(call=id_call).consolidacion
        return consolidacion
