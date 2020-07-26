from django.urls import path

from appointments.views import office

urlpatterns = [
    path('', office.AppointmentListView.as_view(), name='office-appointments'),
    path('<int:pk>/update/', office.AppointmentUpdateView.as_view(), name='office-appointment-change'),
    path('<int:pk>/delete/', office.AppointmentDeleteView.as_view(), name='office-appointment-delete'),
]
