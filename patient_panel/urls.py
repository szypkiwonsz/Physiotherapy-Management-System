from django.urls import include, path
from . import views

urlpatterns = [
    path('', views.patient_home, name='patient-home'),
    path('appointment/', include('appointments.urls')),
    ]
