from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.shortcuts import redirect
from django.shortcuts import render
from django.template.loader import render_to_string
from django.urls import reverse, reverse_lazy
from django.utils.decorators import method_decorator
from django.views.generic import CreateView, UpdateView, DeleteView, DetailView, View

from applications.medical_history.forms import MedicalHistoryForm
from applications.medical_history.models import MedicalHistory
from applications.users.decorators import office_required
from utils.paginate import paginate


@method_decorator([login_required, office_required], name='dispatch')
class MedicalHistoryListView(View):
    model = MedicalHistory
    template_name = 'medical_history/office/medical_history.html'

    def get(self, request):
        """Function override due to adding pagination and search."""
        url_without_parameters = str(request.get_full_path()).split('?')[0]
        url_parameter_q = request.GET.get('q')
        if url_parameter_q:
            ctx = {
                'medical_histories': MedicalHistory.objects.filter(
                    owner=self.request.user.id, patient__last_name__icontains=url_parameter_q).order_by(
                    '-date_selected'
                ),
            }
        else:
            ctx = {
                'medical_histories': MedicalHistory.objects.filter(owner=self.request.user.id).order_by(
                    '-date_selected'
                ),
            }
            paginated_medical_histories = paginate(request, ctx['medical_histories'], 10)

            ctx = {
                'medical_histories': paginated_medical_histories,
                'endpoint': url_without_parameters
            }

        if request.is_ajax():
            html = render_to_string(
                template_name='medical_history/office/medical_history_results_partial.html',
                context=ctx
            )
            data_dict = {"html_from_view": html}
            return JsonResponse(data=data_dict, safe=False)
        return render(request, self.template_name, ctx)


@method_decorator([login_required, office_required], name='dispatch')
class MakeMedicalHistory(CreateView):
    form_class = MedicalHistoryForm
    template_name = 'medical_history/office/medical_history_add_form.html'

    def get_form_kwargs(self, *args, **kwargs):
        kwargs = super(MakeMedicalHistory, self).get_form_kwargs()
        kwargs['user'] = self.request.user
        return kwargs

    def get_context_data(self, **kwargs):
        context = super(MakeMedicalHistory, self).get_context_data(**kwargs)
        context['previous_url'] = self.request.META.get('HTTP_REFERER')
        return context

    def form_valid(self, form):
        post = form.save(commit=False)
        post.owner_id = self.request.user.id
        post.save()
        return redirect('office_panel:medical_history:list')


@method_decorator([login_required, office_required], name='dispatch')
class MedicalHistoryDetailView(DetailView):
    form_class = MedicalHistory
    template_name = 'medical_history/office/medical_history_detail_form.html'

    def get_queryset(self):
        return MedicalHistory.objects.all()

    def get_success_url(self):
        return reverse('office_panel:patient_update', kwargs={'pk': self.object.pk})


@method_decorator([login_required, office_required], name='dispatch')
class MedicalHistoryUpdateView(UpdateView):
    form_class = MedicalHistoryForm
    template_name = 'medical_history/office/medical_history_update_form.html'

    def get_form_kwargs(self, *args, **kwargs):
        kwargs = super(MedicalHistoryUpdateView, self).get_form_kwargs()
        kwargs['user'] = self.request.user
        return kwargs

    def get_context_data(self, **kwargs):
        context = super(MedicalHistoryUpdateView, self).get_context_data(**kwargs)
        context['previous_url'] = self.request.META.get('HTTP_REFERER')
        return context

    def get_queryset(self):
        return MedicalHistory.objects.filter(owner=self.request.user.id)

    def get_success_url(self):
        return reverse('office_panel:medical_history:list')


@method_decorator([login_required, office_required], name='dispatch')
class MedicalHistoryDeleteView(DeleteView):
    template_name = 'medical_history/office/medical_history_delete_confirm.html'
    success_url = reverse_lazy('office_panel:medical_history:list')

    def get_context_data(self, **kwargs):
        context = super(MedicalHistoryDeleteView, self).get_context_data(**kwargs)
        context['previous_url'] = self.request.META.get('HTTP_REFERER')
        return context

    def delete(self, request, *args, **kwargs):
        messages.success(request, f'Wizyta została poprawnie usunięta.')
        return super().delete(request, *args, **kwargs)

    def get_queryset(self):
        return MedicalHistory.objects.filter(owner=self.request.user.id)
