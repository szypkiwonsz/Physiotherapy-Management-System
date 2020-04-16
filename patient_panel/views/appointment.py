from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db.models import Count
from django.shortcuts import render
from django.urls import reverse_lazy, reverse
from django.utils.decorators import method_decorator
from django.views import View
from django.views.generic import DeleteView, UpdateView
from appointments.models import Appointment
from appointments.forms import AppointmentForm
from users.decorators import patient_required


class AppointmentCancelView(DeleteView):
    model = Appointment
    context_object_name = 'appointment'
    template_name = 'patient_panel/appointment_cancel_confirm.html'
    success_url = reverse_lazy('patient-appointment-upcoming')

    def delete(self, request, *args, **kwargs):
        appointment = self.get_object()
        messages.success(request, f'Wizyta w gabinecie: {appointment.office.name}, została pomyślnie odwołana.')
        return super().delete(request, *args, **kwargs)

    def get_queryset(self):
        name = self.request.user.id
        return Appointment.objects.filter(owner=name)


@method_decorator([login_required, patient_required], name='dispatch')
class AppointmentListView(View):
    model = Appointment
    ordering = ('date', )
    template_name = 'patient_panel/appointments_upcoming.html'

    def get_queryset(self):
        queryset = self.request.user.appointments \
            .select_related('owner') \
            .annotate(questions_count=Count('owner', distinct=True)) \
            # .annotate(taken_count=Count('taken_quizzes', distinct=True))
        return queryset

    def get(self, request):
        context = {
            'appointments': self.get_queryset(),
            # 'form': self.post(request)
        }
        return render(request, 'patient_panel/appointments_upcoming.html', context)


@method_decorator([login_required, patient_required], name='dispatch')
class AppointmentUpdateView(UpdateView):
    form_class = AppointmentForm
    context_object_name = 'appointment'
    initial = {'form': 'form'}
    template_name = 'patient_panel/appointment_update_form.html'

    # def get_context_data(self, **kwargs):
    #     kwargs['first_name'] = self.get_object().first_name.annotate()
    #     return super().get_context_data(**kwargs)

    def get_queryset(self):
        name = self.request.user.id
        return Appointment.objects.filter(owner=name)

    def get_success_url(self):
        return reverse('patient-appointment-change', kwargs={'pk': self.object.pk})
