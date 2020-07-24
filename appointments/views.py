from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.utils.decorators import method_decorator
from django.views import View
from django.views.generic import CreateView

from users.decorators import patient_required
from users.models import Office
from utils.send_email import appointment_confirmation_patient, appointment_confirmation_office
from .forms import AppointmentPatientMakeForm
from .models import Appointment


@method_decorator([login_required, patient_required], name='dispatch')
class SelectOffice(View):
    model = Office
    template_name = 'appointments/patient_appointment_select_office.html'

    def get(self, request):
        context = {
            'offices': Office.objects.all()
        }
        return render(request, self.template_name, context)


@method_decorator([login_required, patient_required], name='dispatch')
class MakeAppointment(CreateView):
    form_class = AppointmentPatientMakeForm
    template_name = 'appointments/patient_appointment_make_form.html'

    def get_owner_id(self):
        return self.request.user.id

    def get_office_id(self):
        url = self.request.get_full_path()
        office_id = int(''.join(i for i in url if i.isdigit()))
        return office_id

    def appointment_wrong_date(self):
        messages.warning(self.request, 'Wybierz poprawną godzinę.')
        return redirect('appointments-make-appointment', self.id_office)

    def appointment_date_taken(self, date, id_office):
        messages.warning(
            self.request, f'Wybrana data {date.day}.{date.month}.{date.year} {date.hour}:00 '
                          f'jest już zajęta.'
        )
        return redirect('appointments-make-appointment', id_office)

    def form_valid(self, form):
        date = form.cleaned_data.get('date')
        name = form.cleaned_data.get('name')

        id_owner = self.get_owner_id()
        id_office = self.get_office_id()

        if date.hour == 0:
            self.appointment_wrong_date()
        else:
            data = Appointment.objects.raw(f'SELECT * FROM appointments_appointment WHERE office_id={id_office}')
            for i in data:
                if date == i.date:
                    self.appointment_date_taken(date, id_office)

        appointment = form.save(commit=False)
        appointment.owner_id = id_owner
        appointment.office_id = id_office
        appointment.save()

        office_email = appointment.office.user.email
        patient_email = self.request.user.email
        appointment_confirmation_office(name, date, office_email)
        appointment_confirmation_patient(name, appointment.office.name, date, patient_email)

        messages.warning(self.request, 'Poprawnie umówiono wizytę, ale oczekuje ona na potwierdzenie.')
        return redirect('patient-appointment-upcoming')
