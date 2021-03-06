from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.shortcuts import redirect, render
from django.template.loader import render_to_string
from django.urls import reverse, reverse_lazy
from django.utils.decorators import method_decorator
from django.views.generic import CreateView, UpdateView, DeleteView, DetailView, ListView

from applications.office_panel.forms import PatientForm
from applications.office_panel.models import Patient
from applications.users.decorators import office_required
from utils.paginate import paginate


@method_decorator([login_required, office_required], name='dispatch')
class PatientListView(ListView):
    model = Patient
    template_name = 'office_panel/patient/patients.html'

    def get_queryset(self):
        queryset = self.request.user.patients.select_related('owner')
        return queryset

    def get(self, request, **kwargs):
        """Function override due to adding pagination and search."""
        url_without_parameters = str(request.get_full_path()).split('?')[0]
        url_parameter_q = request.GET.get('q')
        if url_parameter_q:
            ctx = {
                'patients': self.get_queryset().order_by('-date_selected').filter(last_name__icontains=url_parameter_q),
            }
        else:
            ctx = {
                'patients': self.get_queryset().order_by('-date_selected'),
            }
            paginated_patients = paginate(request, ctx['patients'], 10)

            ctx = {
                'patients': paginated_patients,
                'endpoint': url_without_parameters
            }

        if request.is_ajax():
            html = render_to_string(
                template_name='office_panel/patient/patients_results_partial.html',
                context=ctx
            )
            data_dict = {"html_from_view": html}
            return JsonResponse(data=data_dict, safe=False)
        return render(request, self.template_name, ctx)


@method_decorator([login_required, office_required], name='dispatch')
class PatientCreateView(CreateView):
    form_class = PatientForm
    template_name = 'office_panel/patient/patient_add_form.html'

    def get_context_data(self, **kwargs):
        context = super(PatientCreateView, self).get_context_data(**kwargs)
        # previous url for back button
        context['previous_url'] = self.request.META.get('HTTP_REFERER')
        return context

    def get_form_kwargs(self, *args, **kwargs):
        kwargs = super(PatientCreateView, self).get_form_kwargs()
        # passing user pk to form
        kwargs['user'] = self.request.user
        return kwargs

    def form_valid(self, form):
        patient = form.save(commit=False)
        patient.owner = self.request.user
        patient.save()
        messages.success(self.request, 'Pacjent został dodany poprawnie.')
        return redirect('office_panel:home')


@method_decorator([login_required, office_required], name='dispatch')
class PatientDetailView(DetailView):
    form_class = PatientForm
    template_name = 'office_panel/patient/patient_detail_form.html'

    def get_queryset(self):
        patients = Patient.objects.all()
        return patients


@method_decorator([login_required, office_required], name='dispatch')
class PatientUpdateView(UpdateView):
    form_class = PatientForm
    template_name = 'office_panel/patient/patient_update_form.html'

    def get_context_data(self, **kwargs):
        context = super(PatientUpdateView, self).get_context_data(**kwargs)
        # previous url for back button
        context['previous_url'] = self.request.META.get('HTTP_REFERER')
        return context

    def get_form_kwargs(self, *args, **kwargs):
        kwargs = super(PatientUpdateView, self).get_form_kwargs()
        # passing user pk to form
        kwargs['user'] = self.request.user
        # passing object pk to form
        kwargs['patient'] = self.object.pk
        return kwargs

    def get_queryset(self):
        return self.request.user.patients.all()

    def get_success_url(self):
        return reverse('office_panel:patients')


@method_decorator([login_required, office_required], name='dispatch')
class PatientDeleteView(DeleteView):
    template_name = 'office_panel/patient/patient_delete_confirm.html'
    success_url = reverse_lazy('office_panel:patients')

    def get_context_data(self, **kwargs):
        context = super(PatientDeleteView, self).get_context_data(**kwargs)
        # previous url for back button
        context['previous_url'] = self.request.META.get('HTTP_REFERER')
        return context

    def delete(self, request, *args, **kwargs):
        patient = self.get_object()
        messages.success(request, f'Pacjent {patient.first_name} został poprawnie usunięty.')
        return super().delete(request, *args, **kwargs)

    def get_queryset(self):
        return self.request.user.patients.all()
