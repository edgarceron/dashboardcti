from django.core.management.base import BaseCommand
from agent_console.console_functions import create_calls_consolidacion

class Command(BaseCommand):
    """Creates the calls for the consolidación modules"""
    def handle(self, *args, **options):
        create_calls_consolidacion.create_calls_consolidacion()
