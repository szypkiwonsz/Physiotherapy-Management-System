from django.urls import path, include

from applications.office_panel.views import home, patient, timetable

app_name = 'office_panel'
urlpatterns = [
    path('', home.OfficePanelView.as_view(), name='home'),
    path('patients/', include([
        path('', patient.PatientListView.as_view(), name='patients'),
        path('add/', patient.PatientCreateView.as_view(), name='patient_add'),
        path('<int:pk>/', patient.PatientDetailView.as_view(), name='patient_detail'),
        path('<int:pk>/update/', patient.PatientUpdateView.as_view(), name='patient_update'),
        path('<int:pk>/delete/', patient.PatientDeleteView.as_view(), name='patient_delete'),
    ])),
    path('medical_history/', include('applications.medical_history.urls.office')),
    path('appointments/', include('applications.appointments.urls.office')),
    path('timetable/', timetable.TimetableView.as_view(), name='timetable')
]
