from django.urls import path

from medical_history.views import patient

app_name = 'medical_history'
urlpatterns = [
    path('', patient.MedicalHistoryListView.as_view(), name='list'),
]
