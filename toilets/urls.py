from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('api/toilets/', views.toilet_data, name='toilet_data'),
    path('report/', views.report_toilet, name='report_toilet'),
    path('report-issue/', views.report_issue, name='report_issue'),
]