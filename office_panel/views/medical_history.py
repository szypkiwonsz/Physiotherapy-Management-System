from django.shortcuts import render
from django.utils.decorators import method_decorator
from django.views import View
from medical_history.models import MedicalHistory
from users.decorators import login_required, office_required


@method_decorator([login_required, office_required], name='dispatch')
class MedicalHistoryListView(View):
    model = MedicalHistory
    template_name = 'office_panel/office_medical_history.html'

    def get(self, request):
        context = {
            'medical_histories': MedicalHistory.objects.filter(owner=self.request.user.id),
        }
        return render(request, 'office_panel/office_medical_history.html', context)
