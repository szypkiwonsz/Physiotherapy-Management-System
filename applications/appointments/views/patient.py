from datetime import datetime

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse, Http404
from django.shortcuts import redirect, render
from django.template.loader import render_to_string
from django.urls import reverse_lazy, reverse
from django.utils.decorators import method_decorator
from django.views.generic import DeleteView, UpdateView, CreateView, ListView

from applications.appointments.forms import AppointmentPatientMakeForm, AppointmentPatientUpdateForm
from applications.appointments.models import Appointment, Service
from applications.appointments.tasks import appointment_confirmation_email_patient, \
    appointment_confirmation_email_office
from applications.appointments.utils import database_old_datetime_format_to_new
from applications.office_panel.utils import get_dates_taken
from applications.users.decorators import patient_required
from applications.users.models import UserOffice, OfficeDay
from utils.office_opening_hours import get_office_opening_hours
from utils.paginate import paginate


@method_decorator([login_required, patient_required], name='dispatch')
class SelectOffice(ListView):
    model = UserOffice
    template_name = 'appointments/patient/appointment_select_office.html'
    context_object_name = 'offices'


@method_decorator([login_required, patient_required], name='dispatch')
class MakeAppointment(CreateView):
    form_class = AppointmentPatientMakeForm
    template_name = 'appointments/patient/appointment_make_form.html'

    def get_context_data(self, **kwargs):
        context = super(MakeAppointment, self).get_context_data(**kwargs)
        context['opening_hours'] = get_office_opening_hours(self.kwargs.get('pk'))
        context['previous_url'] = self.request.META.get('HTTP_REFERER')
        return context

    def form_valid(self, form):
        datetime_form_value = form.cleaned_data.get('date')
        patient_first_name = form.cleaned_data.get('first_name')

        appointment = form.save(commit=False)
        appointment.owner_id = self.request.user.id
        appointment.office_id = self.kwargs.get('pk')
        appointment.patient_email = self.request.user.email
        service = Service.objects.get(office=self.kwargs.get('pk'), name=form.cleaned_data.get('service'))
        appointment.service = service
        appointment.save()

        office_email = appointment.office.user.email
        patient_email = self.request.user.email

        date = datetime_form_value.strftime('%d.%m.%Y')
        time = datetime_form_value.strftime('%H:%M')
        # sending email as celery task
        appointment_confirmation_email_office.delay(
            patient_first_name, date, time, office_email
        )
        # sending email as celery task
        appointment_confirmation_email_patient.delay(
            patient_first_name, appointment.office.name, date, time,
            patient_email
        )

        messages.warning(self.request, 'Poprawnie umówiono wizytę, ale oczekuje ona na potwierdzenie.')
        return redirect('patient_panel:appointments:upcoming')

    def get_form_kwargs(self, *args, **kwargs):
        """Overriding the method to send the date from the url to the form."""
        kwargs = super(MakeAppointment, self).get_form_kwargs()
        # passing office pk to form
        kwargs['office'] = self.kwargs.get('pk')
        date = self.kwargs.get('date')
        service = self.kwargs.get('service')
        services = Service.objects.values_list('name', flat=True).filter(office=self.kwargs.get('pk'))
        if service not in services:
            raise Http404
        service_obj = Service.objects.filter(name=service, office=self.kwargs.get('pk')).first()
        date_database_format = datetime.strptime(date, '%d.%m.%Y %H:%M')
        dates_taken = Appointment.objects.filter(office=self.kwargs.get('pk'))
        dates_taken = get_dates_taken(dates_taken, service_obj)
        if date in dates_taken:
            # if date from url is taken raise 404 error (in case the user changes the url)
            raise Http404
        office_day = OfficeDay.objects.get(office=self.kwargs.get('pk'), day=date_database_format.weekday())
        if int(office_day.earliest_appointment_time.split(':')[0]) > int(date[-5:-3]) or \
                int(office_day.latest_appointment_time.split(':')[0]) < int(date[-5:-3]):
            # if the visit time given in the url is smaller or greater than the possibility of making an appointment
            # raise 404 error (in case the user changes the url)
            raise Http404
        if datetime.strptime(date.split(' ')[0], "%d.%m.%Y").date() < datetime.today().date():
            raise Http404
        kwargs['date'] = date
        kwargs['service'] = service_obj
        return kwargs


@method_decorator([login_required, patient_required], name='dispatch')
class AppointmentListView(ListView):
    model = Appointment
    template_name = 'appointments/patient/appointments_upcoming.html'
    context_object_name = 'appointments'

    def get_queryset(self):
        queryset = Appointment.objects.order_by('date') \
            .filter(date__gte=datetime.today(), patient_email=self.request.user.email)
        return queryset

    def get(self, request, **kwargs):
        """Function override due to adding pagination and search."""
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
        queryset = Appointment.objects.order_by('date') \
            .filter(date__lte=datetime.today(), patient_email=self.request.user.email)
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
        return Appointment.objects.filter(patient_email=self.request.user.email)


@method_decorator([login_required, patient_required], name='dispatch')
class AppointmentUpdateView(UpdateView):
    form_class = AppointmentPatientUpdateForm
    template_name = 'appointments/patient/appointment_update_form.html'

    def get_context_data(self, **kwargs):
        context = super(AppointmentUpdateView, self).get_context_data(**kwargs)
        context['previous_url'] = self.request.META.get('HTTP_REFERER')
        context['opening_hours'] = get_office_opening_hours(self.object.office.pk)
        context['appointment_time_interval'] = UserOffice.objects.values_list(
            'appointment_time_interval', flat=True).filter(pk=self.object.office.pk).first()
        return context

    def get_form_kwargs(self, *args, **kwargs):
        kwargs = super(AppointmentUpdateView, self).get_form_kwargs()
        # passing office pk to form
        kwargs['office'] = self.object.office.pk
        # passing appointment object pk to form
        kwargs['appointment'] = self.object.pk
        return kwargs

    def get_initial(self):
        """Replacing the initialized date due to an error with the date saving."""
        initial = super().get_initial()
        date = str(Appointment.objects.filter(id=self.object.pk).values_list('date').get()[0])
        date_object = database_old_datetime_format_to_new(date)
        initial['date'] = date_object
        service_name = Appointment.objects.get(office=self.object.office, pk=self.object.pk).service.name
        initial['service'] = Service.objects.get(name=service_name, office=self.object.office)
        return initial

    def form_valid(self, form):
        appointment = Appointment.objects.get(pk=self.object.pk)
        appointment.confirmed = False
        appointment.date = form.cleaned_data['date']
        appointment.first_name = form.cleaned_data['first_name']
        appointment.last_name = form.cleaned_data['last_name']
        appointment.phone_number = form.cleaned_data['phone_number']
        appointment.service = form.cleaned_data['service']
        appointment.save()
        return redirect(self.get_success_url())

    def get_queryset(self):
        return Appointment.objects.filter(patient_email=self.request.user.email)

    def get_success_url(self):
        return reverse('patient_panel:appointments:upcoming')
