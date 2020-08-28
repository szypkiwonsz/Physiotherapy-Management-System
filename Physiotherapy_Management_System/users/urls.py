from django.contrib.auth import views as auth_views
from django.urls import path, re_path, include

from users.views import signup, activate_account, password, profile

app_name = 'users'
urlpatterns = [
    re_path(r'^activate/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$',
            activate_account.activate, name='activate'),
    re_path(r'^reset/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$',
            password.NewPasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    path('signup/', include([
        path('', signup.Register.as_view(), name='signup'),
        path('patient/', signup.RegisterPatient.as_view(), name='patient_signup'),
        path('office/', signup.RegisterOffice.as_view(), name='office_signup'),
    ])),
    path('profile/', include([
        path('office/', profile.OfficeProfile.as_view(), name='office_profile'),
        path('patient/', profile.PatientProfile.as_view(), name='patient_profile'),
    ]))
]
