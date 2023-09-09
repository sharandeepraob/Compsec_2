# yourapp/management/commands/run_as_executable.py
from django.core.management.base import BaseCommand
from django.core.management import call_command
from django.core.wsgi import get_wsgi_application
from django.conf import settings
import os

class Command(BaseCommand):
    help = 'Run Django app as a standalone executable'

    def handle(self, *args, **options):
        os.environ.setdefault("DJANGO_SETTINGS_MODULE", "exeapp.settings")
        application = get_wsgi_application()
        call_command('runserver', '127.0.0.1:8000/')
        print('connecting')
