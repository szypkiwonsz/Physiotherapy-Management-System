from django.urls import path

from appointments.views import patient

urlpatterns = [
    path('select/', patient.SelectOffice.as_view(), name='appointments-select'),
    path('old/', patient.OldAppointmentListView.as_view(), name='patient-appointment-old'),
    path('upcoming/', patient.AppointmentListView.as_view(), name='patient-appointment-upcoming'),
    path('<int:pk>/change/', patient.AppointmentUpdateView.as_view(), name='patient-appointment-change'),
    path('<int:pk>/cancel/', patient.AppointmentCancelView.as_view(), name='patient-appointment-cancel'),
    path('<int:pk>/make/', patient.MakeAppointment.as_view(), name='appointments-make-appointment'),
]
