from datetime import datetime
import time
import pytz
from django.test import SimpleTestCase
from django.db import connections
from _thread import start_new_thread
from agent_console.console_functions.generate_users import GenerateUsers
from agent_console.models import *

class AgentConsoleServerTest(SimpleTestCase):
    databases = {'default', 'call_center'}

    def test_auto_generate_users(self):
        agent = Agent(
            type='Agent',
            number='110',
            name='Mauro',
            password='Mauro',
            estatus='A',
            eccp_password='aaaa'
        )
        agent.save()

        agent = Agent(
            type='Agent',
            number='111',
            name='Karlos',
            password='Mauro',
            estatus='A',
            eccp_password='aaaa'
        )
        agent.save()

        GenerateUsers.bulk_create_users()

        count = User.objects.count()
        self.assertEqual(count, 2)

        user_agent = UserAgent.objects.get(agent=agent.id)
        user = user_agent.user
        expected = agent.number + "@call.center"
        self.assertEqual(user.username, expected)
