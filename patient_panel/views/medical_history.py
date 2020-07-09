from django.shortcuts import render
from django.utils.decorators import method_decorator
from django.views import View
from medical_history.models import MedicalHistory
from users.decorators import login_required, patient_required


@method_decorator([login_required, patient_required], name='dispatch')
class MedicalHistoryListView(View):
    model = MedicalHistory
    template_name = 'patient_panel/patient_medical_history.html'

    def get_queryset(self):
        queryset = MedicalHistory.objects.filter(patient__email=self.request.user).order_by('-date_selected')
        return queryset

    def get(self, request):
        context = {
            'medical_histories': self.get_queryset(),
        }
        return render(request, 'patient_panel/patient_medical_history.html', context)
