import os
import sys
import django
from django.conf import settings

def pytest_configure():
    sys.path.insert(0, os.path.abspath(os.path.dirname(__file__)))
    settings.DEBUG = False
    django.setup() 