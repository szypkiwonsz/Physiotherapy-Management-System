from datetime import datetime

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.exceptions import ObjectDoesNotExist
from django.http import JsonResponse
from django.shortcuts import redirect, render
from django.template.loader import render_to_string
from django.urls import reverse_lazy, reverse
from django.utils.decorators import method_decorator
from django.views.generic import DeleteView, UpdateView, CreateView, ListView

from applications.appointments.forms import AppointmentPatientMakeForm
from applications.appointments.models import Appointment
from applications.appointments.tasks import appointment_confirmation_email_patient, \
    appointment_confirmation_email_office
from applications.appointments.utils import database_old_datetime_format_to_new
from applications.users.decorators import patient_required
from applications.users.models import Office
from utils.add_zero import add_zero
from utils.paginate import paginate


@method_decorator([login_required, patient_required], name='dispatch')
class SelectOffice(ListView):
    model = Office
    template_name = 'appointments/patient/appointment_select_office.html'
    context_object_name = 'offices'


@method_decorator([login_required, patient_required], name='dispatch')
class MakeAppointment(CreateView):
    form_class = AppointmentPatientMakeForm
    template_name = 'appointments/patient/appointment_make_form.html'

    def appointment_date_taken(self, date):
        messages.warning(
            self.request,
            f'Wybrana data {add_zero(date.day)}.{add_zero(date.month)}.{date.year} {date.hour}:00 '
            f'jest już zajęta.'
        )

    @staticmethod
    def date_and_time_from_datetime(datetime_value):
        date_and_time = str(datetime_value).split(' ')
        date = date_and_time[0].split('-')
        time = date_and_time[1].split(':')
        return date, time

    def form_valid(self, form):
        datetime_form_value = form.cleaned_data.get('date')
        if datetime_form_value.hour == 0:
            messages.warning(self.request, 'Wybierz poprawną godzinę.')
            return redirect('patient_panel:appointments:make', pk=self.kwargs.get('pk'))
        else:
            appointment = Appointment.objects.filter(date=datetime_form_value)
            if appointment:
                self.appointment_date_taken(datetime_form_value)
                return redirect('patient_panel:appointments:make', pk=self.kwargs.get('pk'))
        date, time = self.date_and_time_from_datetime(datetime_form_value)
        name = form.cleaned_data.get('name')
        appointment = form.save(commit=False)
        appointment.owner_id = self.request.user.id
        appointment.office_id = self.kwargs.get('pk')
        appointment.save()

        office_email = appointment.office.user.email
        patient_email = self.request.user.email
        appointment_confirmation_email_office.delay(name, date, time, office_email)
        appointment_confirmation_email_patient.delay(name, appointment.office.name, date, time, patient_email)

        messages.warning(self.request, 'Poprawnie umówiono wizytę, ale oczekuje ona na potwierdzenie.')
        return redirect('patient_panel:appointments:upcoming')


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
        """
        Function override due to adding pagination and search.
        """
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
            paginated_appointments = paginate(request, ctx['appointments'], 10)

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
    template_name = 'appointments/patient/appointment_cancel_confirm.html'
    success_url = reverse_lazy('patient_panel:appointments:upcoming')

    def get_context_data(self, **kwargs):
        context = super(AppointmentCancelView, self).get_context_data(**kwargs)
        context['previous_url'] = self.request.META.get('HTTP_REFERER')
        return context

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

    def get_context_data(self, **kwargs):
        context = super(AppointmentUpdateView, self).get_context_data(**kwargs)
        context['previous_url'] = self.request.META.get('HTTP_REFERER')
        return context

    def appointment_date_taken(self, date):
        messages.warning(
            self.request,
            f'Wybrana data {add_zero(date.day)}.{add_zero(date.month)}.{date.year} {date.hour}:00 '
            f'jest już zajęta.'
        )

    def get_initial(self):
        """
        Replacing the initialized date due to an error with the date saving.
        """
        initial = super().get_initial()
        date = str(Appointment.objects.filter(id=self.object.pk).values_list('date').get()[0])
        date_object = database_old_datetime_format_to_new(date)
        initial['date'] = date_object
        return initial

    def form_valid(self, form):
        appointment = Appointment.objects.get(pk=self.object.pk)
        if appointment.date.hour == 0:
            messages.warning(self.request, 'Wybierz poprawną godzinę.')
            return redirect('patient_panel:appointments:update', pk=self.object.pk)
        else:
            try:
                appointment_check = Appointment.objects.get(date=form.cleaned_data['date'])
            except ObjectDoesNotExist:
                appointment_check = None
            if appointment_check and appointment_check.pk != self.object.pk:
                self.appointment_date_taken(appointment.date)
                return redirect('patient_panel:appointments:update', self.object.pk)
        appointment.confirmed = False
        appointment.date = form.cleaned_data['date']
        appointment.name = form.cleaned_data['name']
        appointment.phone_number = form.cleaned_data['phone_number']
        appointment.choice = form.cleaned_data['choice']
        appointment.save()
        return redirect(self.get_success_url())

    def get_queryset(self):
        return Appointment.objects.filter(owner=self.request.user.id)

    def get_success_url(self):
        return reverse('patient_panel:appointments:upcoming')
