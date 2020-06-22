from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect
from django.shortcuts import render
from django.urls import reverse, reverse_lazy
from django.utils.decorators import method_decorator
from django.views import View
from django.views.generic import CreateView, UpdateView, DeleteView, DetailView

from medical_history.forms import MedicalHistoryForm
from medical_history.models import MedicalHistory
from users.decorators import office_required


@method_decorator([login_required, office_required], name='dispatch')
class MedicalHistoryListView(View):
    model = MedicalHistory
    template_name = 'office_panel/office_medical_history.html'

    def get(self, request):
        context = {
            'medical_histories': MedicalHistory.objects.filter(owner=self.request.user.id),
        }
        return render(request, 'office_panel/office_medical_history.html', context)


@method_decorator([login_required, office_required], name='dispatch')
class MakeMedicalHistory(CreateView):
    form_class = MedicalHistoryForm
    template_name = 'medical_history/medical_history_add_form.html'

    def form_valid(self, form):
        post = form.save(commit=False)
        post.owner_id = self.request.user.id
        post.save()
        return redirect('office-medical-history')


@method_decorator([login_required, office_required], name='dispatch')
class MedicalHistoryDetailView(DetailView):
    form_class = MedicalHistory
    template_name = 'medical_history/medical_history_detail_form.html'

    def get_queryset(self):
        return MedicalHistory.objects.all()

    def get_success_url(self):
        return reverse('office-patient-change', kwargs={'pk': self.object.pk})


@method_decorator([login_required, office_required], name='dispatch')
class MedicalHistoryUpdateView(UpdateView):
    form_class = MedicalHistoryForm
    template_name = 'medical_history/medical_history_update_form.html'

    def get_queryset(self):
        return MedicalHistory.objects.filter(owner=self.request.user.id)

    def get_success_url(self):
        return reverse('office-medical-history-change', kwargs={'pk': self.object.pk})


@method_decorator([login_required, office_required], name='dispatch')
class MedicalHistoryDeleteView(DeleteView):
    form_class = MedicalHistoryForm
    template_name = 'medical_history/medical_history_delete_confirm.html'
    success_url = reverse_lazy('office-medical-history')

    def delete(self, request, *args, **kwargs):
        messages.success(request, f'Wizyta została poprawnie usunięta.')
        return super().delete(request, *args, **kwargs)

    def get_queryset(self):
        return MedicalHistory.objects.filter(owner=self.request.user.id)
