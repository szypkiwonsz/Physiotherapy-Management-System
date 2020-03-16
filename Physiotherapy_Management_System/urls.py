from django.contrib import admin
from django.urls import path, include
from users.views import signup, login
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('', include('home_page.urls')),
    path('panel/', login.check_user, name='panel'),
    path('patient/', include('patient_panel.urls')),
    path('office/', include('office_panel.urls')),
    path('admin/', admin.site.urls),
    path('accounts/login/', auth_views.LoginView.as_view(template_name='users/login.html'), name='login'),
    path('accounts/logout/', auth_views.LogoutView.as_view(template_name='users/login.html'), name='logout'),
    path('accounts/signup/', signup.SignUpView.as_view(), name='signup'),
]
