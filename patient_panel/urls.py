from django.urls import include, path
from patient_panel.views import home, appointment

urlpatterns = [
    path('', home.PatientHome.as_view(), name='patient-home'),
    path('appointments/', include('appointments.urls')),
    path('appointment/upcoming', appointment.AppointmentListView.as_view(), name='patient-appointment-upcoming'),
    path('appointment/<int:pk>/', appointment.AppointmentUpdateView.as_view(), name='patient-appointment-change'),
    path('appointment/<int:pk>/cancel/', appointment.AppointmentCancelView.as_view(), name='patient-appointment-cancel'
         ),
    ]
