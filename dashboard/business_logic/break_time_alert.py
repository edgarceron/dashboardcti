import pytz
import pendulum
from datetime import timedelta, datetime
from agent_console.models import Audit, Break, BreakTimes, Agent
from agent_console.console_functions.agent_state import AgentState


def get_break_time_alerts():
    """Return info about the agent that have exceeded the break allowed time"""
    active_agents = Audit.objects.filter(id_break__isnull=True, datetime_end__isnull=True)
    today_aware = pendulum.instance(datetime.now(), 'UTC')
    alerts = []
    for agent in active_agents:
        active_break = AgentState.get_active_break(agent.id_agent, agent.datetime_init)
        if active_break != None:
            try:
                init = active_break.datetime_init
                timezone = pytz.timezone("America/Bogota")
                init = init.replace(tzinfo=timezone)
                init = pendulum.instance(init)
                total = (today_aware - init).in_seconds()
                allowed = BreakTimes.objects.get(id_break=active_break.id_break.id).minutes
                remain = timedelta(minutes=allowed).seconds - total
                agent = Agent.objects.get(pk=active_break.id_agent.id)
                if remain < 0:
                    total = -1 * remain
                    alerts.append({
                        'agent': agent.name,
                        'number': agent.number,
                        'off': total})
            except Agent.DoesNotExist:
                pass
            except BreakTimes.DoesNotExist:
                pass
    return alerts
