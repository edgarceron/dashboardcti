from django.core.management.base import BaseCommand
from agent_console.console_functions import set_made_calls

class Command(BaseCommand):
    """Command for setting maded calls between db"""
    def handle(self, *args, **options):
        set_made_calls.set_made_calls()
