from django.urls import path
from home_page.views import HomeView, OfficesView, HelpView

urlpatterns = [
    path('', HomeView.as_view(), name='home'),
    path('help/', HelpView.as_view(), name='help'),
    path('offices/', OfficesView.as_view(), name='offices')
    ]
