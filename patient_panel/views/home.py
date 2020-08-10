from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from django.utils.decorators import method_decorator
from django.views import View

from appointments.models import Appointment
from medical_history.models import MedicalHistory
from users.decorators import patient_required
from users.models import Office


@method_decorator([login_required, patient_required], name='dispatch')
class PatientHome(View):
    template_name = 'patient_panel/home.html'

    def get(self, request):
        context = {
            'offices': Office.objects.filter(user__patients__email=self.request.user)[:5],
            'appointments': Appointment.objects.filter(owner=self.request.user).order_by('date')[:5],
            'medical_histories': MedicalHistory.objects.filter(patient__email=self.request.user).order_by(
                '-date_selected')[:5]
        }
        return render(request, self.template_name, context)
