import os
from django.core.wsgi import get_wsgi_application
from whitenoise import WhiteNoise # Bu satır kritik

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'freetoilet_project.settings')

application = get_wsgi_application()

# Statik dosyaların toplandığı klasörü WhiteNoise'a tanıtıyoruz
# BASE_DIR'deki 'staticfiles' klasörüne bakmasını söylüyoruz
base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
application = WhiteNoise(application, root=os.path.join(base_dir, 'staticfiles'))

# Vercel'in çalıştırdığı değişken
app = application