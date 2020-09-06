from django.urls import path, include

from medical_history.views import office

app_name = 'medical_history'
urlpatterns = [
    path('', office.MedicalHistoryListView.as_view(), name='list'),
    path('add/', office.MakeMedicalHistory.as_view(), name='make'),
    path('<int:pk>/', include([
        path('', office.MedicalHistoryDetailView.as_view(), name='detail'),
        path('update/', office.MedicalHistoryUpdateView.as_view(), name='update'),
        path('delete/', office.MedicalHistoryDeleteView.as_view(), name='delete')
    ]))
]
