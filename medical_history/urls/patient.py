from django.urls import path

from medical_history.views import patient

urlpatterns = [
    path('', patient.MedicalHistoryListView.as_view(), name='patient-medical-history'),
]
