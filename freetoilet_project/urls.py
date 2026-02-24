from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    # Gelen trafiği 'toilets' uygulamasının urls.py dosyasına aktar
    path('', include('toilets.urls')), 
]