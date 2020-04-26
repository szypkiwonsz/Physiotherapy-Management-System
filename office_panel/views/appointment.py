from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from django.urls import reverse, reverse_lazy
from django.utils.decorators import method_decorator
from django.views import View
from django.views.generic import UpdateView, DeleteView
from appointments.models import Appointment
from users.decorators import office_required


@method_decorator([login_required, office_required], name='dispatch')
class AppointmentListView(View):
    model = Appointment
    template_name = 'office_panel/office-appointments.html'

    def get(self, request):
        context = {
            'appointments': Appointment.objects.filter(office=self.request.user.id),
        }
        return render(request, 'office_panel/office-appointments.html', context)


class AppointmentUpdateView(UpdateView):
    model = Appointment
    fields = ('date', 'confirmed')
    template_name = 'office_panel/appointment_update_form.html'

    def get_queryset(self):
        return Appointment.objects.filter(office=self.request.user.id)

    def get_success_url(self):
        return reverse('office-appointment-change', kwargs={'pk': self.object.pk})


class AppointmentDeleteView(DeleteView):
    model = Appointment
    template_name = 'office_panel/appointment_delete_confirm.html'
    success_url = reverse_lazy('office-appointments')

    def delete(self, request, *args, **kwargs):
        appointment = self.get_object()
        messages.success(request, f'Wizyta {appointment.name} została poprawnie usunięta.')
        return super().delete(request, *args, **kwargs)

    def get_queryset(self):
        return Appointment.objects.filter(office=self.request.user.id)
