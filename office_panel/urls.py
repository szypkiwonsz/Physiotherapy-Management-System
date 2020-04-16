from django.urls import path
from office_panel.views import home, patient, appointment
from medical_history import views as medical_history_view

urlpatterns = [
    path('', home.PatientListView.as_view(), name='office-home'),
    path('patients/', patient.PatientListView.as_view(), name='office-patients'),
    path('patients/add/', patient.PatientCreateView.as_view(), name='office-patient-add'),
    path('patients/<int:pk>/', patient.PatientUpdateView.as_view(), name='office-patient-change'),
    path('patients/<int:pk>/delete/', patient.PatientDeleteView.as_view(), name='office-patient-delete-confirm'),
    path('appointments/', appointment.AppointmentListView.as_view(), name='office-appointments'),
    path('appointments/<int:pk>/', appointment.AppointmentUpdateView.as_view(), name='office-appointment-change'),
    path('appointments/<int:pk>/delete/', appointment.AppointmentDeleteView.as_view(), name='office-appointment-delete'),
    path('medical_history/<int:pk>/', medical_history_view.MakeMedicalHistory.as_view(),
         name='office-make-medical-history'),
    ]
