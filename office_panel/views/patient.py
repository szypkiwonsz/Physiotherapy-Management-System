from django.db.models import Count
from django.shortcuts import redirect, render
from django.urls import reverse, reverse_lazy
from django.views.generic import CreateView, View, UpdateView, DeleteView
from users.models import Patient
from django.contrib import messages


class PatientCreateView(CreateView):
    model = Patient
    fields = ('first_name', 'last_name', 'email')
    template_name = 'office_panel/patient_add_form.html'

    def form_valid(self, form):
        patient = form.save(commit=False)
        patient.owner = self.request.user
        patient.save()
        messages.success(self.request, 'The patient was created with success! Go ahead and add some questions now.')
        return redirect('office-home')


class PatientListView(View):
    model = Patient
    ordering = ('owner', )
    template_name = 'office_panel/office_patients.html'

    def get_queryset(self):
        queryset = self.request.user.patients \
            .select_related('owner') \
            .annotate(questions_count=Count('first_name', distinct=True)) \
            # .annotate(taken_count=Count('taken_quizzes', distinct=True))
        return queryset

    def get(self, request):
        context = {
            'patients': self.get_queryset(),
            # 'form': self.post(request)
        }
        if request.user.is_office:
            return render(request, 'office_panel/office_patients.html', context)
        else:
            messages.warning(request, "Musisz być zalogowany jako gabinet by mieć dostęp do tej strony.")
            return redirect('patient-home')


class PatientUpdateView(UpdateView):
    model = Patient
    fields = ('first_name', 'last_name', 'email', )
    context_object_name = 'patient'
    template_name = 'office_panel/patient_update_form.html'

    # def get_context_data(self, **kwargs):
    #     kwargs['first_name'] = self.get_object().first_name.annotate()
    #     return super().get_context_data(**kwargs)

    def get_queryset(self):
        '''
        This method is an implicit object-level permission management
        This view will only match the ids of existing quizzes that belongs
        to the logged in user.
        '''
        return self.request.user.patients.all()

    def get_success_url(self):
        return reverse('office-patient-change', kwargs={'pk': self.object.pk})


class PatientDeleteView(DeleteView):
    model = Patient
    context_object_name = 'patient'
    template_name = 'office_panel/patient_delete_confirm.html'

    def delete(self, request, *args, **kwargs):
        patient = self.get_object()
        messages.success(request, 'The quiz %s was deleted with success!' % patient.first_name)
        return super().delete(request, *args, **kwargs)

    def get_queryset(self):
        return self.request.user.patients.all()

    def get_success_url(self):
        return reverse('office-patient-change', kwargs={'pk': self.object.pk})
