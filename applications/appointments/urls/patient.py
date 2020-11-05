from django.urls import path, include

from applications.appointments.views import patient

app_name = 'appointments'
urlpatterns = [
    path('select/', patient.SelectOffice.as_view(), name='select'),
    path('old/', patient.OldAppointmentListView.as_view(), name='old'),
    path('upcoming/', patient.AppointmentListView.as_view(), name='upcoming'),
    path('<int:pk>/', include([
        path('change/', patient.AppointmentUpdateView.as_view(), name='update'),
        path('cancel/', patient.AppointmentCancelView.as_view(), name='delete'),
        path('make/', patient.MakeAppointment.as_view(), name='make')
    ]))
]
