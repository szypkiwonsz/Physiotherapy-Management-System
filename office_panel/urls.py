from django.urls import path
from office_panel.views import home, patient

urlpatterns = [
    path('', home.PatientListView.as_view(), name='office-home'),
    path('patients/', patient.PatientListView.as_view(), name='office-patients'),
    path('patients/add/', patient.PatientCreateView.as_view(), name='office-patient-add'),
    path('patients/<int:pk>/', patient.PatientUpdateView.as_view(), name='office-patient-change'),
    path('patients/<int:pk>/delete/', patient.PatientDeleteView.as_view(), name='office-patient-delete-confirm'),
    ]
