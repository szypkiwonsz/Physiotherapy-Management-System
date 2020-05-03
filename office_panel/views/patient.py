from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render
from django.urls import reverse, reverse_lazy
from django.contrib import messages
from django.utils.decorators import method_decorator
from django.views.generic import CreateView, View, UpdateView, DeleteView, DetailView
from users.decorators import office_required
from users.forms import PatientForm
from medical_history.models import MedicalHistory
from users.models import Patient


@method_decorator([login_required, office_required], name='dispatch')
class PatientListView(View):
    form_class = PatientForm
    template_name = 'office_panel/office_patients.html'

    def get_queryset(self):
        queryset = self.request.user.patients.select_related('owner')
        return queryset

    def get(self, request):
        context = {
            'patients': self.get_queryset(),
            'medical_history': MedicalHistory.objects.all()
        }
        return render(request, 'office_panel/office_patients.html', context)


@method_decorator([login_required, office_required], name='dispatch')
class PatientCreateView(CreateView):
    form_class = PatientForm
    template_name = 'office_panel/patient_add_form.html'

    def form_valid(self, form):
        patient = form.save(commit=False)
        patient.owner = self.request.user
        patient.save()
        messages.success(self.request, 'Pacjent został dodany poprawnie.')
        return redirect('office-home')


@method_decorator([login_required, office_required], name='dispatch')
class PatientDetailView(DetailView):
    form_class = PatientForm
    template_name = 'office_panel/patient_detail_form.html'

    def get_queryset(self):
        patients = Patient.objects.all()
        return patients

    def get_success_url(self):
        return reverse('office-patient-change', kwargs={'pk': self.object.pk})


@method_decorator([login_required, office_required], name='dispatch')
class PatientUpdateView(UpdateView):
    form_class = PatientForm
    template_name = 'office_panel/patient_update_form.html'

    def get_queryset(self):
        return self.request.user.patients.all()

    def get_success_url(self):
        return reverse('office-patient-change', kwargs={'pk': self.object.pk})


@method_decorator([login_required, office_required], name='dispatch')
class PatientDeleteView(DeleteView):
    form_class = PatientForm
    template_name = 'office_panel/patient_delete_confirm.html'
    success_url = reverse_lazy('office-patients')

    def delete(self, request, *args, **kwargs):
        patient = self.get_object()
        messages.success(request, f'Pacjent {patient.first_name} został poprawnie usunięty.')
        return super().delete(request, *args, **kwargs)

    def get_queryset(self):
        return self.request.user.patients.all()
