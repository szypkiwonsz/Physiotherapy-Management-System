from django.contrib import messages
from django.shortcuts import render, redirect
from django.urls import reverse, reverse_lazy
from django.views import View
from django.views.generic import UpdateView, DeleteView

from appointments.models import Appointment


class AppointmentListView(View):
    model = Appointment
    ordering = ('owner', )
    template_name = 'office_panel/office-appointments.html'

    def get_queryset(self):
        name = self.request.user.id
        queryset = Appointment.objects.filter(office=name)
        return queryset

    def get(self, request):
        context = {
            'appointments': self.get_queryset(),
            # 'form': self.post(request)
        }
        if request.user.is_office:
            return render(request, 'office_panel/office-appointments.html', context)
        else:
            messages.warning(request, "Musisz być zalogowany jako gabinet by mieć dostęp do tej strony.")
            return redirect('patient-home')


class AppointmentUpdateView(UpdateView):
    model = Appointment
    fields = ('date', 'confirmed')
    context_object_name = 'appointment'
    template_name = 'office_panel/appointment_update_form.html'

    # def get_context_data(self, **kwargs):
    #     kwargs['first_name'] = self.get_object().first_name.annotate()
    #     return super().get_context_data(**kwargs)

    def get_queryset(self):
        '''
        This method is an implicit object-level permission management
        This view will only match the ids of existing quizzes that belongs
        to the logged in user.
        '''
        name = self.request.user.id
        return Appointment.objects.filter(office=name)

    def get_success_url(self):
        return reverse('office-appointment-change', kwargs={'pk': self.object.pk})


class AppointmentDeleteView(DeleteView):
    model = Appointment
    context_object_name = 'appointment'
    template_name = 'office_panel/appointment_delete_confirm.html'
    success_url = reverse_lazy('office-appointments')

    def delete(self, request, *args, **kwargs):
        appointment = self.get_object()
        messages.success(request, 'The quiz %s was deleted with success!' % appointment.name)
        return super().delete(request, *args, **kwargs)

    def get_queryset(self):
        name = self.request.user.id
        return Appointment.objects.filter(office=name)
