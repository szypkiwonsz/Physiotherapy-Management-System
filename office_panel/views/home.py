from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from django.utils.decorators import method_decorator
from django.views import View
from users.decorators import office_required
from users.models import Patient
from appointments.models import Appointment
from medical_history.models import MedicalHistory


@method_decorator([login_required, office_required], name='dispatch')
class OfficePanelView(View):
    model = Patient
    template_name = 'office_panel/office_home.html'

    def get(self, request):
        context = {
            'patients': Patient.objects.filter(owner=self.request.user.id)[:5],
            'appointments': Appointment.objects.filter(office=self.request.user.id)[:5],
            'medical_histories': MedicalHistory.objects.filter(owner=self.request.user.id)[:5]
        }
        return render(request, 'office_panel/office_home.html', context)
