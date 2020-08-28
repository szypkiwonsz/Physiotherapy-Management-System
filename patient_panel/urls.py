from django.urls import include, path

from patient_panel.views import home, offices

app_name = 'patient_panel'
urlpatterns = [
    path('', home.PatientHome.as_view(), name='home'),
    path('offices/', offices.OfficesListView.as_view(), name='offices'),
    path('medical_history/', include('medical_history.urls.patient')),
    path('appointments/', include('appointments.urls.patient')),
]
