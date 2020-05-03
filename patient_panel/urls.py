from django.urls import include, path
from patient_panel.views import home, appointment, offices, medical_history

urlpatterns = [
    path('', home.PatientHome.as_view(), name='patient-home'),
    path('offices/', offices.OfficesListView.as_view(), name='patient-offices'),
    path('medical_histories/', medical_history.MedicalHistoryListView.as_view(), name='patient-medical-history'),
    path('appointments/', include('appointments.urls')),
    path('appointment/upcoming', appointment.AppointmentListView.as_view(), name='patient-appointment-upcoming'),
    path('appointment/old', appointment.OldAppointmentListView.as_view(), name='patient-appointment-old'),
    path('appointment/<int:pk>/', appointment.AppointmentUpdateView.as_view(), name='patient-appointment-change'),
    path('appointment/<int:pk>/cancel/', appointment.AppointmentCancelView.as_view(), name='patient-appointment-cancel'
         ),
]
