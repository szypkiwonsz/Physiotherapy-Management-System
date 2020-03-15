from django.contrib import admin
from django.urls import path
from users.views import offices

urlpatterns = [
    path('admin/', admin.site.urls),
    path('accounts/signup/office/', offices.SignUpView.as_view(), name='signup'),
]
