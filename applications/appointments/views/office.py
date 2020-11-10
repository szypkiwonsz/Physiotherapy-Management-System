import datetime

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse, Http404
from django.shortcuts import render, redirect
from django.template.loader import render_to_string
from django.urls import reverse, reverse_lazy
from django.utils.decorators import method_decorator
from django.views import View
from django.views.generic import UpdateView, DeleteView, CreateView

from applications.appointments.forms import AppointmentOfficeUpdateForm, AppointmentOfficeMakeForm
from applications.appointments.models import Appointment
from applications.appointments.utils import database_old_datetime_format_to_new
from applications.users.decorators import office_required
from utils.paginate import paginate


@method_decorator([login_required, office_required], name='dispatch')
class AppointmentListView(View):
    model = Appointment
    template_name = 'appointments/office/appointments.html'

    def get(self, request):
        """
        Function override due to adding pagination and search.
        """
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

    def get_initial(self):
        """
        Replacing the initialized date due to an error with the date saving.
        """
        initial = super().get_initial()
        date = str(Appointment.objects.filter(id=self.object.pk).values_list('date').get()[0])
        date_object = database_old_datetime_format_to_new(date)
        initial['date'] = date_object
        return initial

    def get_context_data(self, **kwargs):
        context = super(AppointmentUpdateView, self).get_context_data(**kwargs)
        context['previous_url'] = self.request.META.get('HTTP_REFERER')
        return context

    def get_queryset(self):
        return Appointment.objects.filter(office=self.request.user.id)

    def get_success_url(self):
        return reverse('office_panel:appointments:list')


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
        messages.success(request, f'Wizyta {appointment.name} została poprawnie usunięta.')
        return super().delete(request, *args, **kwargs)

    def get_queryset(self):
        return Appointment.objects.filter(office=self.request.user.id)


class MakeAppointment(CreateView):
    form_class = AppointmentOfficeMakeForm
    template_name = 'appointments/office/appointment_make_form.html'
    success_url = reverse_lazy('office_panel:appointments:list')

    def form_valid(self, form):
        appointment = form.save(commit=False)
        appointment.first_name = form.cleaned_data.get('patient').first_name
        appointment.last_name = form.cleaned_data.get('patient').last_name
        appointment.owner = self.request.user
        appointment.office_id = self.kwargs.get('pk')
        appointment.patient_email = form.cleaned_data.get('patient').email
        appointment.save()
        return redirect('office_panel:appointments:list')

    def get_form_kwargs(self, *args, **kwargs):
        kwargs = super(MakeAppointment, self).get_form_kwargs()
        date = self.request.GET['date']
        date_database_format = datetime.datetime.strptime(date, '%d.%m.%Y %H:%M')
        if Appointment.objects.filter(date=date_database_format):
            # if date from url is taken raise 404 error (in case the user changes the url)
            raise Http404
        if int(self.request.session['hour_open']) > int(self.request.GET['date'][-5:-3]) or \
                int(self.request.session['hour_close']) <= int(self.request.GET['date'][-5:-3]):
            # if the visit time given in the url is smaller or greater than the possibility of making an appointment
            # raise 404 error (in case the user changes the url)
            raise Http404
        kwargs['user'] = self.request.user
        kwargs['date'] = date
        return kwargs
