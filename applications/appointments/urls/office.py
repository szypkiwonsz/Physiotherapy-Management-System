from django.urls import path, include

from applications.appointments.views import office

app_name = 'appointments'
urlpatterns = [
    path('', office.AppointmentListView.as_view(), name='list'),
    path('<int:pk>/', include([
        path('update/', office.AppointmentUpdateView.as_view(), name='update'),
        path('delete/', office.AppointmentDeleteView.as_view(), name='delete'),
        path('make/', office.MakeAppointment.as_view(), name='make')
    ]))
]
