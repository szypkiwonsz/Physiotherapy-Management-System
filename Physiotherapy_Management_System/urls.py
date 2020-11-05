from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.contrib.auth import views as auth_views
from django.urls import path, include

from applications.users.views import login

urlpatterns = [
    path('', include('applications.home_page.urls')),
    path('login/', login.LoginView.as_view(), name='login'),
    path('logout/', auth_views.LogoutView.as_view(template_name='users/logout.html'), name='logout'),
    path('panel/', login.CheckUser.as_view(), name='panel'),
    path('patient/', include('applications.patient_panel.urls')),
    path('office/', include('applications.office_panel.urls')),
    path('accounts/', include('applications.users.urls')),
    path('admin/', admin.site.urls),
    path('password/', include([
        path('reset/', auth_views.PasswordResetView.as_view(), name='password_reset'),
        path('reset/done/', auth_views.PasswordResetDoneView.as_view(), name='password_reset_done'),
        path('reset/complete/', auth_views.PasswordResetCompleteView.as_view(), name='password_reset_complete'),
    ]))
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
