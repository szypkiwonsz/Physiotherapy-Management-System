from django.urls import include, path
from . import views

urlpatterns = [
    path('', views.office_home, name='office-home'),

    ]