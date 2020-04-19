from django.urls import path
from .views import HomeView, Offices

urlpatterns = [
    path('', HomeView.as_view(), name='home'),
    path('offices/', Offices.as_view(), name='offices')
    ]
