from django.urls import path, include

from applications.appointments.views import office, timetable
from applications.users.decorators import office_required, login_required

app_name = 'appointments'
urlpatterns = [
    path('', office.AppointmentListView.as_view(), name='list'),
    path('timetable/', login_required(office_required(timetable.TimetableView.as_view())), name='timetable'),
    path('<int:pk>/', include([
        path('update/', office.AppointmentUpdateView.as_view(), name='update'),
        path('delete/', office.AppointmentDeleteView.as_view(), name='delete'),
        path('make/', office.MakeAppointment.as_view(), name='make')
    ]))
]
