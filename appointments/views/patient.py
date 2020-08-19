from datetime import datetime

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.exceptions import ObjectDoesNotExist
from django.http import HttpResponseRedirect, HttpResponse, JsonResponse
from django.shortcuts import redirect, render
from django.template.loader import render_to_string
from django.urls import reverse_lazy, reverse
from django.utils.decorators import method_decorator
from django.views.generic import DeleteView, UpdateView, CreateView, ListView

from appointments.forms import AppointmentPatientMakeForm
from appointments.models import Appointment
from users.decorators import patient_required
from users.models import Office, User
from utils.date_time import DateTime
from utils.paginate import paginate
from utils.send_email import appointment_confirmation_patient, appointment_confirmation_office


@method_decorator([login_required, patient_required], name='dispatch')
class SelectOffice(ListView):
    model = Office
    template_name = 'appointments/patient/appointment_select_office.html'
    context_object_name = 'offices'


@method_decorator([login_required, patient_required], name='dispatch')
class MakeAppointment(CreateView):
    form_class = AppointmentPatientMakeForm
    template_name = 'appointments/patient/appointment_make_form.html'

    def get(self, request, *args, **kwargs):
        id_office = self.get_office_id()
        user = User.objects.get(id=id_office)
        if user.is_patient:
            return HttpResponse(status=404)
        else:
            context = {'form': self.form_class}
            return render(request, self.template_name, context)

    def get_owner_id(self):
        return self.request.user.id

    def get_office_id(self):
        url = self.request.get_full_path()
        office_id = int(''.join(i for i in url if i.isdigit()))
        return office_id

    def appointment_date_taken(self, date):
        messages.warning(
            self.request,
            f'Wybrana data {DateTime.add_zero(date.day)}.{DateTime.add_zero(date.month)}.{date.year} {date.hour}:00 '
            f'jest już zajęta.'
        )

    def form_valid(self, form):
        date = form.cleaned_data.get('date')
        name = form.cleaned_data.get('name')
        id_owner = self.get_owner_id()
        id_office = self.get_office_id()
        if date.hour == 0:
            messages.warning(self.request, 'Wybierz poprawną godzinę.')
            return redirect('appointments-make-appointment', id_office)
        else:
            appointment = Appointment.objects.filter(date=date)
            if appointment:
                self.appointment_date_taken(date)
                return redirect('appointments-make-appointment', id_office)
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


@method_decorator([login_required, patient_required], name='dispatch')
class AppointmentListView(ListView):
    model = Appointment
    template_name = 'appointments/patient/appointments_upcoming.html'
    context_object_name = 'appointments'

    def get_queryset(self):
        queryset = self.request.user.appointments.select_related('owner').order_by('date') \
            .filter(date__gte=datetime.today())
        return queryset

    def get(self, request, **kwargs):
        url_without_parameters = str(request.get_full_path()).split('?')[0]
        url_parameter_q = request.GET.get('q')
        if url_parameter_q:
            ctx = {
                'appointments': self.get_queryset().filter(office__name__icontains=url_parameter_q),
            }
        else:
            ctx = {
                'appointments': self.get_queryset(),
            }
            paginated_appointments = paginate(request, ctx['appointments'], 2)

            ctx = {
                'appointments': paginated_appointments,
                'endpoint': url_without_parameters
            }

        if request.is_ajax():
            html = render_to_string(
                template_name='appointments/patient/appointments_upcoming_results_partial.html',
                context=ctx
            )
            data_dict = {"html_from_view": html}
            return JsonResponse(data=data_dict, safe=False)
        return render(request, self.template_name, ctx)


@method_decorator([login_required, patient_required], name='dispatch')
class OldAppointmentListView(ListView):
    model = Appointment
    template_name = 'appointments/patient/appointments_old.html'
    context_object_name = 'appointments'

    def get_queryset(self):
        queryset = self.request.user.appointments.select_related('owner').order_by('date') \
            .filter(date__lte=datetime.today())
        return queryset


@method_decorator([login_required, patient_required], name='dispatch')
class AppointmentCancelView(DeleteView):
    model = Appointment
    template_name = 'appointments/patient/appointment_cancel_confirm.html'
    success_url = reverse_lazy('patient-appointment-upcoming')

    def delete(self, request, *args, **kwargs):
        appointment = self.get_object()
        messages.success(request, f'Wizyta w gabinecie: {appointment.office.name}, została pomyślnie odwołana.')
        return super().delete(request, *args, **kwargs)

    def get_queryset(self):
        return Appointment.objects.filter(owner=self.request.user.id)


@method_decorator([login_required, patient_required], name='dispatch')
class AppointmentUpdateView(UpdateView):
    form_class = AppointmentPatientMakeForm
    template_name = 'appointments/patient/appointment_update_form.html'

    def appointment_date_taken(self, date):
        messages.warning(
            self.request,
            f'Wybrana data {DateTime.add_zero(date.day)}.{DateTime.add_zero(date.month)}.{date.year} {date.hour}:00 '
            f'jest już zajęta.'
        )

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

    def form_valid(self, form):
        appointment = Appointment.objects.get(pk=self.object.pk)
        appointment.confirmed = False
        appointment.date = form.cleaned_data['date']
        id_appointment = appointment.pk
        if appointment.date.hour == 0:
            self.appointment_wrong_date()
        else:
            try:
                appointment_check = Appointment.objects.get(date=appointment.date)
            except ObjectDoesNotExist:
                appointment_check = None
            if appointment_check and appointment_check.pk != id_appointment:
                self.appointment_date_taken(appointment.date)
                return redirect('patient-appointment-change', id_appointment)
        appointment.name = form.cleaned_data['name']
        appointment.phone_number = form.cleaned_data['phone_number']
        appointment.choice = form.cleaned_data['choice']
        appointment.save()
        return HttpResponseRedirect(self.get_success_url())

    def get_queryset(self):
        return Appointment.objects.filter(owner=self.request.user.id)

    def get_success_url(self):
        return reverse('patient-appointment-change', kwargs={'pk': self.object.pk})
