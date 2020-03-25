from django.contrib import admin
from django.urls import path, include, re_path
from users.views import signup, login, activate_account
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('', include('home_page.urls')),
    path('panel/', login.check_user, name='panel'),
    path('patient/', include('patient_panel.urls')),
    path('office/', include('office_panel.urls')),
    path('admin/', admin.site.urls),
    path('accounts/login/', login.Login.as_view(), name='login'),
    path('accounts/logout/', auth_views.LogoutView.as_view(template_name='users/login.html'), name='logout'),
    path('accounts/signup/patient/', signup.RegisterPatient.as_view(), name='patient-signup'),
    path('accounts/signup/office/', signup.RegisterOffice.as_view(), name='office-signup'),
    re_path(r'^activate/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$',
            activate_account.activate, name='activate')
]
