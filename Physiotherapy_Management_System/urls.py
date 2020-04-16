from django.contrib import admin
from django.urls import path, include
from users.views import login
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('', include('home_page.urls')),
    path('panel/', login.CheckUser.as_view(), name='panel'),
    path('patient/', include('patient_panel.urls')),
    path('office/', include('office_panel.urls')),
    path('account/', include('users.urls')),
    path('admin/', admin.site.urls),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
