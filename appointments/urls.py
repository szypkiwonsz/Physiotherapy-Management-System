from django.urls import path
from . import views

urlpatterns = [
    path('', views.AppointmentListView.as_view(), name='appointments-home'),
    path('select/', views.SelectOffice.as_view(), name='appointments-select'),
    path('<int:pk>/', views.MakeAppointment.as_view(), name='appointments-make-appointment'),
    path('cancel_appointment/', views.cancel_appointment, name='appointments-cancel_appointment')
]
