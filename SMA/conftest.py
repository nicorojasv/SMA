import os
import sys
import django
from django.conf import settings

def pytest_configure():
    # Agregar el directorio del proyecto al PYTHONPATH
    sys.path.insert(0, os.path.abspath(os.path.dirname(__file__)))
    # Configurar Django
    os.environ['DJANGO_SETTINGS_MODULE'] = 'SMA.settings'
    settings.DEBUG = False
    django.setup() 