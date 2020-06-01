from datetime import datetime
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from django.urls import reverse_lazy, reverse
from django.utils.decorators import method_decorator
from django.views import View
from django.views.generic import DeleteView, UpdateView
from appointments.models import Appointment
from appointments.forms import AppointmentForm
from users.decorators import patient_required


@method_decorator([login_required, patient_required], name='dispatch')
class AppointmentListView(View):
    model = Appointment
    template_name = 'patient_panel/appointments_upcoming.html'

    def get_queryset(self):
        queryset = self.request.user.appointments.select_related('owner').order_by('date') \
            .filter(date__gte=datetime.today())
        return queryset

    def get(self, request):
        context = {
            'appointments': self.get_queryset(),
        }
        return render(request, 'patient_panel/appointments_upcoming.html', context)


@method_decorator([login_required, patient_required], name='dispatch')
class OldAppointmentListView(View):
    model = Appointment
    template_name = 'patient_panel/appointments_old.html'

    def get_queryset(self):
        queryset = self.request.user.appointments.select_related('owner').order_by('date') \
            .filter(date__lte=datetime.today())
        return queryset

    def get(self, request):
        context = {
            'appointments': self.get_queryset(),
        }
        return render(request, 'patient_panel/appointments_old.html', context)


@method_decorator([login_required, patient_required], name='dispatch')
class AppointmentCancelView(DeleteView):
    model = Appointment
    template_name = 'patient_panel/appointment_cancel_confirm.html'
    success_url = reverse_lazy('patient-appointment-upcoming')

    def delete(self, request, *args, **kwargs):
        appointment = self.get_object()
        messages.success(request, f'Wizyta w gabinecie: {appointment.office.name}, została pomyślnie odwołana.')
        return super().delete(request, *args, **kwargs)

    def get_queryset(self):
        return Appointment.objects.filter(owner=self.request.user.id)


@method_decorator([login_required, patient_required], name='dispatch')
class AppointmentUpdateView(UpdateView):
    form_class = AppointmentForm
    template_name = 'patient_panel/appointment_update_form.html'

    @staticmethod
    def parse_db_time_string(time_string):
        date = datetime.strptime(time_string.split('+')[0], '%Y-%m-%d %H:%M:%S')
        return datetime.strftime(date, '%d.%m.%Y %H:%M')

    def get_initial(self):
        initial = super().get_initial()
        date = str(Appointment.objects.filter(id=self.object.pk).values_list('date').get()[0])
        date_object = self.parse_db_time_string(date)
        initial['date'] = date_object
        return initial

    def get_queryset(self):
        return Appointment.objects.filter(owner=self.request.user.id)

    def get_success_url(self):
        return reverse('patient-appointment-change', kwargs={'pk': self.object.pk})
