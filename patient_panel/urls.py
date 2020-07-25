from django.urls import include, path
from patient_panel.views import home, offices, medical_history

urlpatterns = [
    path('', home.PatientHome.as_view(), name='patient-home'),
    path('offices/', offices.OfficesListView.as_view(), name='patient-offices'),
    path('medical_histories/', medical_history.MedicalHistoryListView.as_view(), name='patient-medical-history'),
    path('appointments/', include('appointments.urls')),
]
