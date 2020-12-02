from django.urls import include, path

from applications.patient_panel.views import home, offices

app_name = 'patient_panel'
urlpatterns = [
    path('', home.PatientHome.as_view(), name='home'),
    path('offices/', offices.OfficesListView.as_view(), name='offices'),
    path('medical_history/', include('applications.medical_history.urls.patient')),
    path('appointments/', include('applications.appointments.urls.patient')),
]
