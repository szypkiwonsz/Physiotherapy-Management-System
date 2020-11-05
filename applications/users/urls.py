from django.urls import path, include

from applications.users.views import signup, activate_account, password, profile

app_name = 'users'
urlpatterns = [
    path('activate/<slug:uidb64>/<slug:token>/',
         activate_account.activate, name='activate'),
    path('reset/<slug:uidb64>/<slug:token>/',
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
