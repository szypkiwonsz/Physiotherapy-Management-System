from django.urls import path
from . import views

urlpatterns = [
    path('', views.make_appointment, name='appointments-make_appointment'),
    path('cancel_appointment/', views.cancel_appointment, name='appointments-cancel_appointment')
]
