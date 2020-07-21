from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.shortcuts import redirect, render
from django.template.loader import render_to_string
from django.urls import reverse, reverse_lazy
from django.utils.decorators import method_decorator
from django.views.generic import CreateView, View, UpdateView, DeleteView, DetailView

from office_panel.models import Patient
from users.decorators import office_required
from users.forms import PatientForm


@method_decorator([login_required, office_required], name='dispatch')
class PatientListView(View):
    form_class = PatientForm
    template_name = 'office_panel/office_patients.html'

    def get_queryset(self):
        queryset = self.request.user.patients.select_related('owner')
        return queryset

    def get(self, request):
        url_parameter = request.GET.get('q')
        if url_parameter:
            ctx = {
                'patients': self.get_queryset().order_by('-date_selected').filter(last_name__icontains=url_parameter),
            }
        else:
            ctx = {
                'patients': self.get_queryset().order_by('-date_selected'),
            }

        if request.is_ajax():
            html = render_to_string(
                template_name='office_panel/office_patients_results_partial.html',
                context=ctx
            )
            data_dict = {"html_from_view": html}
            return JsonResponse(data=data_dict, safe=False)

        return render(request, 'office_panel/office_patients.html', ctx)


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
