from django.urls import path
from office_panel.views import home, patient, appointment, medical_history

urlpatterns = [
    path('', home.OfficePanelView.as_view(), name='office-home'),
    path('patients/', patient.PatientListView.as_view(), name='office-patients'),
    path('patients/add/', patient.PatientCreateView.as_view(), name='office-patient-add'),
    path('patients/<int:pk>/', patient.PatientDetailView.as_view(), name='office-patient-detail'),
    path('patients/<int:pk>/update/', patient.PatientUpdateView.as_view(), name='office-patient-change'),
    path('patients/<int:pk>/delete/', patient.PatientDeleteView.as_view(), name='office-patient-delete-confirm'),
    path('appointments/', appointment.AppointmentListView.as_view(), name='office-appointments'),
    path('appointments/<int:pk>/', appointment.AppointmentUpdateView.as_view(), name='office-appointment-change'),
    path('appointments/<int:pk>/delete/', appointment.AppointmentDeleteView.as_view(),
         name='office-appointment-delete'),
    path('medical_history/', medical_history.MedicalHistoryListView.as_view(), name='office-medical-history'),
    path('medical_history/<int:pk>/', medical_history.MedicalHistoryDetailView.as_view(),
         name='office-medical-history-detail'),
    path('medical_history/add/', medical_history.MakeMedicalHistory.as_view(), name='office-make-medical-history'),
    path('medical_history/<int:pk>/update/', medical_history.MedicalHistoryUpdateView.as_view(),
         name='office-medical-history-change'),
    path('medical_history/<int:pk>/delete/', medical_history.MedicalHistoryDeleteView.as_view(),
         name='office-medical-history-delete')
]
