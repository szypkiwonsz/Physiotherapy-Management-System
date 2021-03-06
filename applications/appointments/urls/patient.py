from django.urls import path, include

from applications.appointments.views import patient
from applications.appointments.views import timetable
from applications.users.decorators import patient_required, login_required

app_name = 'appointments'
urlpatterns = [
    path('select/', patient.SelectOffice.as_view(), name='select'),
    path('old/', patient.OldAppointmentListView.as_view(), name='old'),
    path('upcoming/', patient.AppointmentListView.as_view(), name='upcoming'),
    path('<int:pk>/', include([
        path('timetable/', login_required(patient_required(timetable.TimetableView.as_view())), name='timetable'),
        path('change/', patient.AppointmentUpdateView.as_view(), name='update'),
        path('cancel/', patient.AppointmentCancelView.as_view(), name='delete'),
        path('<str:date>/<str:service>/make/', patient.MakeAppointment.as_view(), name='make')
    ]))
]
