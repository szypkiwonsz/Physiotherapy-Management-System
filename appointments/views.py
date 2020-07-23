from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.utils.decorators import method_decorator
from django.views import View
from django.views.generic import CreateView

from users.decorators import patient_required
from users.models import Office
from utils.send_email import appointment_confirmation_patient, appointment_confirmation_office
from .forms import AppointmentForm
from .models import Appointment


@method_decorator([login_required, patient_required], name='dispatch')
class SelectOffice(View):
    model = Office
    template_name = 'appointments/patient_appointment_select_office.html'

    @staticmethod
    def get(request):
        context = {
            'offices': Office.objects.all()
        }
        return render(request, 'appointments/patient_appointment_select_office.html', context)


@method_decorator([login_required, patient_required], name='dispatch')
class MakeAppointment(CreateView):
    form_class = AppointmentForm
    template_name = 'appointments/patient_appointment_make_form.html'

    def form_valid(self, form):
        date = form.cleaned_data.get('date')
        name = form.cleaned_data.get('name')

        id_owner = self.request.user.id
        url = self.request.get_full_path()
        id_office = int(''.join(i for i in url if i.isdigit()))

        if date.hour == 0:
            messages.warning(self.request, 'Wybierz poprawną godzinę.')
            return redirect('appointments-make-appointment', id_office)

        # Checks if first name is typed correctly without any numbers etc.
        elif name.isalpha() is not True:
            messages.warning(self.request, f'Nieprawidłowe imię.')
            return redirect('appointments-make-appointment', id_office)

        else:
            data = Appointment.objects.raw(f'select * FROM appointments_appointment where office_id = {id_office}')
            for i in data:
                if date == i.date:
                    messages.warning(
                        self.request, f'Wybrana data {date.day}.{date.month}.{date.year} {date.hour}:00 '
                                      f'jest już zajęta.'
                    )
                    return redirect('appointments-make-appointment', id_office)
        appointment = form.save(commit=False)
        appointment.author_id = self.request.user.id
        appointment.owner_id = id_owner
        appointment.office_id = id_office
        appointment.save()
        office_email = appointment.office.user.email
        patient_email = self.request.user.email
        appointment_confirmation_office(name, date, office_email)
        appointment_confirmation_patient(name, appointment.office.name, date, patient_email)
        messages.warning(self.request, 'Poprawnie umówiono wizytę, ale oczekuje ona na potwierdzenie.')
        return redirect('patient-appointment-upcoming')
