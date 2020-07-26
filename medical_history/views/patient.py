from django.utils.decorators import method_decorator
from django.views.generic import ListView

from medical_history.models import MedicalHistory
from users.decorators import login_required, patient_required


@method_decorator([login_required, patient_required], name='dispatch')
class MedicalHistoryListView(ListView):
    model = MedicalHistory
    template_name = 'medical_history/patient/medical_history.html'
    context_object_name = 'medical_histories'

    def get_queryset(self):
        queryset = MedicalHistory.objects.filter(patient__email=self.request.user).order_by('-date_selected')
        return queryset
