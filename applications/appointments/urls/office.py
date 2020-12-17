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
        path('<str:date>/<str:service>/make/', office.MakeAppointment.as_view(), name='make')
    ])),
    path('services/', include([
        path('', office.ServiceListView.as_view(), name='service_list'),
        path('add', office.AddServiceView.as_view(), name='service_add'),
        path('<int:pk>/', include([
            path('edit', office.ServiceUpdateView.as_view(), name='service_edit'),
            path('delete', office.ServiceDeleteView.as_view(), name='service_delete')
        ])),
    ]))
]
