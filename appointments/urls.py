from django.urls import path
from . import views

urlpatterns = [
    path('', views.MakeAppointment.as_view(), name='make-appointment'),
    path('cancel_appointment/', views.cancel_appointment, name='appointments-cancel_appointment')
]
