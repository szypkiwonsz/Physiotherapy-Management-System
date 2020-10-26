from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.shortcuts import render
from django.template.loader import render_to_string
from django.urls import reverse, reverse_lazy
from django.utils.decorators import method_decorator
from django.views import View
from django.views.generic import UpdateView, DeleteView

from appointments.forms import AppointmentOfficeUpdateForm
from appointments.models import Appointment
from appointments.utils import database_old_datetime_format_to_new
from users.decorators import office_required
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
                    office=self.request.user.id, owner__email__icontains=url_parameter_q).order_by('date'),
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

    def get_queryset(self):
        return Appointment.objects.filter(office=self.request.user.id)

    def get_success_url(self):
        return reverse('office_panel:appointments:update', kwargs={'pk': self.object.pk})


@method_decorator([login_required, office_required], name='dispatch')
class AppointmentDeleteView(DeleteView):
    model = Appointment
    template_name = 'appointments/office/appointment_delete_confirm.html'
    success_url = reverse_lazy('office_panel:appointments:list')

    def delete(self, request, *args, **kwargs):
        appointment = self.get_object()
        messages.success(request, f'Wizyta {appointment.name} została poprawnie usunięta.')
        return super().delete(request, *args, **kwargs)

    def get_queryset(self):
        return Appointment.objects.filter(office=self.request.user.id)
