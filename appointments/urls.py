from django.urls import path

from . import views

urlpatterns = [
    path('select/', views.SelectOffice.as_view(), name='appointments-select'),
    path('<int:pk>/', views.MakeAppointment.as_view(), name='appointments-make-appointment'),
]
