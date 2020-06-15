from django.test import TestCase
from agent_console.socket_call_entry import socket_server
from agent_console.models import *
# Create your tests here.
class UserModelTest(TestCase):
    databases = {'default', 'call_center'}
    def test_agent_exist(self):

        print("--------------------------------------------------")
        print(self.databases)
        print("--------------------------------------------------")
        agent = Agent(
            type='Agent',
            number='110',
            name='Mauro',
            password='Mauro',
            estatus='A',
            eccp_password='aaaa'
        )

        agent.save()

        result = socket_server.agent_exist(agent.id)

        self.assertEqual(result, True)