# freetoilet_project/wsgi.py

import os
from django.core.wsgi import get_wsgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'freetoilet_project.settings')

application = get_wsgi_application()

# Vercel'in beklentisi olan şu satırı ekliyoruz:
app = application