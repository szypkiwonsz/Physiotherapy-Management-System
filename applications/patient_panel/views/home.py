from datetime import datetime

from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from django.utils.decorators import method_decorator
from django.views import View

from applications.appointments.models import Appointment
from applications.medical_history.models import MedicalHistory
from applications.users.decorators import patient_required
from applications.users.models import UserOffice


@method_decorator([login_required, patient_required], name='dispatch')
class PatientHome(View):
    template_name = 'patient_panel/home.html'

    def get(self, request):
        context = {
            'offices': UserOffice.objects.filter(user__patients__email=self.request.user).distinct()[:5],
            'appointments': Appointment.objects.filter(patient_email=self.request.user.email).order_by('date').filter(
                date__gte=datetime.today())[:5],
            'medical_histories': MedicalHistory.objects.filter(patient__email=self.request.user).order_by(
                '-date_selected')[:5]
        }
        return render(request, self.template_name, context)
