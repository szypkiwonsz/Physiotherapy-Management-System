from django.urls import path

from medical_history.views import office

urlpatterns = [
    path('', office.MedicalHistoryListView.as_view(), name='office-medical-history'),
    path('<int:pk>/', office.MedicalHistoryDetailView.as_view(), name='office-medical-history-detail'),
    path('add/', office.MakeMedicalHistory.as_view(), name='office-make-medical-history'),
    path('<int:pk>/update/', office.MedicalHistoryUpdateView.as_view(), name='office-medical-history-change'),
    path('<int:pk>/delete/', office.MedicalHistoryDeleteView.as_view(), name='office-medical-history-delete')
]
