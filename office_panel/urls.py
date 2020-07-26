from django.urls import path, include
from office_panel.views import home, patient

urlpatterns = [
    path('', home.OfficePanelView.as_view(), name='office-home'),
    path('patients/', patient.PatientListView.as_view(), name='office-patients'),
    path('patients/add/', patient.PatientCreateView.as_view(), name='office-patient-add'),
    path('patients/<int:pk>/', patient.PatientDetailView.as_view(), name='office-patient-detail'),
    path('patients/<int:pk>/update/', patient.PatientUpdateView.as_view(), name='office-patient-change'),
    path('patients/<int:pk>/delete/', patient.PatientDeleteView.as_view(), name='office-patient-delete-confirm'),
    path('medical_history/', include('medical_history.urls.office')),
    path('appointments/', include('appointments.urls.office')),
]
