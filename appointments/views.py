from django.contrib.auth.decorators import login_required
from django.db.models import Count
from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.urls import reverse
from django.utils.decorators import method_decorator
from django.views.generic import UpdateView, CreateView

from .forms import AppointmentForm, AppointmentCancel
from .models import Appointment
from .methods import DateTime
from django.core.mail import EmailMessage
from users.decorators import patient_required
from django.views import View
from users.models import Office


class Appointments:
    @staticmethod
    def send_email(office_name, office_email, date, name):
        subject = 'Appointment - {}'.format(office_name)
        message = '{} was appointed for {}:{} on day {}.{}.{}. ' \
                  'Confirm the visit in the admin panel.'.format(name, DateTime.add_zero(date.hour),
                                                                 DateTime.add_zero(date.minute),
                                                                 DateTime.add_zero(date.day),
                                                                 DateTime.add_zero(date.month),
                                                                 DateTime.add_zero(date.year))
        email = EmailMessage(subject, message, to=[office_email])
        email.send()
        # author_email = User.objects.filter(is_active=True).values_list('email', flat=True)
        subject = 'Your appointments on fizjo-med has been correctly arranged'
        message = 'You have been correctly arranged to visit for {}:{} on day {}.{}.{}. ' \
                  'If you want to cancel your visit, use the form on our website.'.format(DateTime.add_zero(date.hour),
                                                                                          DateTime.add_zero(date.minute),
                                                                                          DateTime.add_zero(date.day),
                                                                                          DateTime.add_zero(date.month),
                                                                                          DateTime.add_zero(date.year))
        email = EmailMessage(subject, message, to=[office_email])
        email.send()


@method_decorator([login_required, patient_required], name='dispatch')
class SelectOffice(View):
    model = Office
    template_name = 'appointment/select_office.html'

    def get(self, request):
        context = {
            'offices': Office.objects.all()
        }
        return render(request, 'appointment/select_office.html', context)


class MakeAppointment(CreateView):
    form_class = AppointmentForm
    template_name = 'appointment/make_appointment.html'

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
            messages.warning(self.request, f'Incorrect name.')
            return redirect('appointments-make-appointment', id_office)

        else:
            data = Appointment.objects.raw(f'select * FROM appointments_appointment where office_id = {id_office}')
            for i in data:
                print(i.office_id)
                if date == i.date:
                    messages.warning(self.request, f'Wybrana data {date.day}.{date.month}.{date.year} {date.hour}:00 jest już zajęta.')
                    return redirect('appointments-make-appointment', id_office)
        appointment = form.save(commit=False)
        appointment.author_id = self.request.user.id
        appointment.owner_id = id_owner
        appointment.office_id = id_office
        appointment.save()
        messages.warning(self.request, 'Poprawnie umówiono wizytę, ale oczekuje ona na potwierdzenie.')
        return redirect('patient-appointment-upcoming')
