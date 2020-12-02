from django.urls import path

from applications.medical_history.views import patient

app_name = 'medical_history'
urlpatterns = [
    path('', patient.MedicalHistoryListView.as_view(), name='list'),
]
