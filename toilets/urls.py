from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('api/toilets/', views.toilet_data, name='toilet_data'),
    # Yeni eklenen satır:
    path('report/', views.report_toilet, name='report_toilet'),
]