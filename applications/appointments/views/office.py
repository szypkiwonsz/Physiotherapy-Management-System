import datetime

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse, Http404
from django.shortcuts import render, redirect
from django.template.loader import render_to_string
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from django.views import View
from django.views.generic import UpdateView, DeleteView, CreateView

from applications.appointments.forms import AppointmentOfficeUpdateForm, AppointmentOfficeMakeForm, ServiceForm
from applications.appointments.models import Appointment
from applications.appointments.models import Service
from applications.appointments.utils import database_old_datetime_format_to_new
from applications.office_panel.utils import get_dates_taken
from applications.users.decorators import office_required
from applications.users.models import OfficeDay, UserOffice
from utils.office_opening_hours import get_office_opening_hours
from utils.paginate import paginate


@method_decorator([login_required, office_required], name='dispatch')
class AppointmentListView(View):
    model = Appointment
    template_name = 'appointments/office/appointments.html'

    def get(self, request):
        """Function override due to adding pagination and search."""
        url_without_parameters = str(request.get_full_path()).split('?')[0]
        url_parameter_q = request.GET.get('q')
        if url_parameter_q:
            ctx = {
                'appointments': Appointment.objects.filter(
                    office=self.request.user.id, last_name__icontains=url_parameter_q).order_by('date'),
            }
        else:
            ctx = {
                'appointments': Appointment.objects.filter(office=self.request.user.id).order_by('date'),
            }
            paginated_appointments = paginate(request, ctx['appointments'], 10)

            ctx = {
                'appointments': paginated_appointments,
                'endpoint': url_without_parameters
            }

        if request.is_ajax():
            html = render_to_string(
                template_name='appointments/office/appointments_results_partial.html',
                context=ctx
            )
            data_dict = {"html_from_view": html}
            return JsonResponse(data=data_dict, safe=False)

        return render(request, self.template_name, ctx)


@method_decorator([login_required, office_required], name='dispatch')
class AppointmentUpdateView(UpdateView):
    form_class = AppointmentOfficeUpdateForm
    template_name = 'appointments/office/appointment_update_form.html'
    success_url = reverse_lazy('office_panel:appointments:list')

    def get_initial(self):
        """Replacing the initialized date due to an error with the date saving."""
        initial = super().get_initial()
        date = str(Appointment.objects.filter(id=self.object.pk).values_list('date').get()[0])
        date_object = database_old_datetime_format_to_new(date)
        service_name = Appointment.objects.get(office=self.request.user.useroffice, pk=self.object.pk).service.name
        initial['date'] = date_object
        initial['service'] = Service.objects.get(name=service_name)
        return initial

    def get_context_data(self, **kwargs):
        context = super(AppointmentUpdateView, self).get_context_data(**kwargs)
        context['previous_url'] = self.request.META.get('HTTP_REFERER')
        context['opening_hours'] = get_office_opening_hours(self.request.user.useroffice)
        context['appointment_time_interval'] = UserOffice.objects.values_list(
            'appointment_time_interval', flat=True).filter(user=self.request.user).first()
        return context

    def get_form_kwargs(self, *args, **kwargs):
        kwargs = super(AppointmentUpdateView, self).get_form_kwargs()
        # passing office pk to form
        kwargs['office'] = self.object.office.pk
        # passing appointment object pk to form
        kwargs['appointment'] = self.object.pk
        # passing service object pk to form
        kwargs['service'] = self.object.service
        return kwargs

    def form_valid(self, form):
        appointment = Appointment.objects.get(pk=self.object.pk)
        appointment.confirmed = form.cleaned_data['confirmed']
        appointment.date = form.cleaned_data['date']
        appointment.service = form.cleaned_data['service']
        appointment.save()
        return redirect(self.get_success_url())

    def get_queryset(self):
        return Appointment.objects.filter(office=self.request.user.id)


@method_decorator([login_required, office_required], name='dispatch')
class AppointmentDeleteView(DeleteView):
    template_name = 'appointments/office/appointment_delete_confirm.html'
    success_url = reverse_lazy('office_panel:appointments:list')

    def get_context_data(self, **kwargs):
        context = super(AppointmentDeleteView, self).get_context_data(**kwargs)
        context['previous_url'] = self.request.META.get('HTTP_REFERER')
        return context

    def delete(self, request, *args, **kwargs):
        appointment = self.get_object()
        messages.success(
            request, f'Wizyta {appointment.first_name} {appointment.last_name} została poprawnie usunięta.'
        )
        return super().delete(request, *args, **kwargs)

    def get_queryset(self):
        return Appointment.objects.filter(office=self.request.user.id)


@method_decorator([login_required, office_required], name='dispatch')
class MakeAppointment(CreateView):
    form_class = AppointmentOfficeMakeForm
    template_name = 'appointments/office/appointment_make_form.html'
    success_url = reverse_lazy('office_panel:appointments:list')

    def get_context_data(self, **kwargs):
        context = super(MakeAppointment, self).get_context_data(**kwargs)
        # previous url for back button.
        context['previous_url'] = self.request.META.get('HTTP_REFERER')
        return context

    def form_valid(self, form):
        appointment = form.save(commit=False)
        appointment.first_name = form.cleaned_data.get('patient').first_name
        appointment.last_name = form.cleaned_data.get('patient').last_name
        appointment.owner = self.request.user
        appointment.office_id = self.kwargs.get('pk')
        appointment.patient_email = form.cleaned_data.get('patient').email
        service = Service.objects.get(name=form.cleaned_data['service'], office=self.kwargs.get('pk'))
        appointment.service = service
        appointment.save()
        return redirect('office_panel:appointments:list')

    def get_form_kwargs(self, *args, **kwargs):
        """Overriding the method to send the date from the url to the form."""
        kwargs = super(MakeAppointment, self).get_form_kwargs()
        # passing office pk to form
        kwargs['office'] = self.request.user.useroffice
        date = self.kwargs.get('date')
        service = self.kwargs.get('service')
        services = Service.objects.values_list('name', flat=True).filter(office=self.request.user.useroffice)
        if service not in services:
            raise Http404
        service_obj = Service.objects.filter(name=service, office=self.request.user.useroffice).first()
        date_database_format = datetime.datetime.strptime(date, '%d.%m.%Y %H:%M')
        dates_taken = Appointment.objects.filter(office=self.request.user.useroffice)
        dates_taken = get_dates_taken(dates_taken, service_obj)
        if date in dates_taken:
            # if date from url is taken raise 404 error (in case the user changes the url)
            raise Http404
        office_day = OfficeDay.objects.get(office=self.request.user.useroffice, day=date_database_format.weekday())
        if int(office_day.earliest_appointment_time.split(':')[0]) > int(date[-5:-3]) or \
                int(office_day.latest_appointment_time.split(':')[0]) < int(date[-5:-3]):
            # if the visit time given in the url is smaller or greater than the possibility of making an appointment
            # raise 404 error (in case the user changes the url)
            raise Http404
        if datetime.datetime.strptime(date.split(' ')[0], "%d.%m.%Y").date() < datetime.datetime.today().date():
            raise Http404
        kwargs['date'] = date
        kwargs['service'] = service_obj
        return kwargs


@method_decorator([login_required, office_required], name='dispatch')
class AddServiceView(CreateView):
    form_class = ServiceForm
    template_name = 'appointments/office/service_add_form.html'

    def get_context_data(self, **kwargs):
        context = super(AddServiceView, self).get_context_data(**kwargs)
        # previous url for back button.
        context['previous_url'] = self.request.META.get('HTTP_REFERER')
        return context

    def form_valid(self, form):
        service = form.save(commit=False)
        service.office_id = self.request.user.useroffice.pk
        service.save()
        messages.success(
            self.request, f'Poprawnie dodałeś nową usługę.'
        )
        return redirect('office_panel:appointments:service_list')


@method_decorator([login_required, office_required], name='dispatch')
class ServiceListView(View):
    model = Service
    template_name = 'appointments/office/services.html'

    def get(self, request):
        """Function override due to adding pagination."""
        services = Service.objects.filter(office=self.request.user.id)
        paginated_services = paginate(request, services, 10)
        ctx = {
            'services': paginated_services,
        }
        return render(request, self.template_name, ctx)


@method_decorator([login_required, office_required], name='dispatch')
class ServiceUpdateView(UpdateView):
    form_class = ServiceForm
    template_name = 'appointments/office/service_update_form.html'
    success_url = reverse_lazy('office_panel:appointments:service_list')

    def get_queryset(self):
        queryset = Service.objects.filter(pk=self.kwargs.get('pk'))
        return queryset

    def get_context_data(self, **kwargs):
        context = super(ServiceUpdateView, self).get_context_data(**kwargs)
        context['previous_url'] = self.request.META.get('HTTP_REFERER')
        return context


@method_decorator([login_required, office_required], name='dispatch')
class ServiceDeleteView(DeleteView):
    model = Service
    template_name = 'appointments/office/service_delete_confirm.html'
    success_url = reverse_lazy('office_panel:appointments:service_list')

    def get_context_data(self, **kwargs):
        context = super(ServiceDeleteView, self).get_context_data(**kwargs)
        context['previous_url'] = self.request.META.get('HTTP_REFERER')
        return context
