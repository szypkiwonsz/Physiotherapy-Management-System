from django.urls import path
from .views import HomeView, Offices, HelpView

urlpatterns = [
    path('', HomeView.as_view(), name='home'),
    path('help/', HelpView.as_view(), name='help'),
    path('offices/', Offices.as_view(), name='offices')
    ]
