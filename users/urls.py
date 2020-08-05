from django.contrib.auth import views as auth_views
from django.urls import path, re_path

from users.views import signup, login, activate_account, password, profile

urlpatterns = [
    path('login/', login.LoginView.as_view(), name='login'),
    path('logout/', auth_views.LogoutView.as_view(template_name='users/logout.html'), name='logout'),
    path('signup/', signup.Register.as_view(), name='signup'),
    path('signup/patient/', signup.RegisterPatient.as_view(), name='patient-signup'),
    path('signup/office/', signup.RegisterOffice.as_view(), name='office-signup'),
    re_path(r'^activate/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$',
            activate_account.activate, name='activate'),
    path('profile/office/', profile.OfficeProfile.as_view(), name='profile-office'),
    path('profile/patient/', profile.PatientProfile.as_view(), name='profile-patient'),
    path('password_reset/', auth_views.PasswordResetView.as_view(), name='password_reset'),
    path('password_reset/done/', auth_views.PasswordResetDoneView.as_view(), name='password_reset_done'),
    re_path(r'^reset/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$',
            password.NewPasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    path('reset/done/', auth_views.PasswordResetCompleteView.as_view(), name='password_reset_complete'),
]
