from django.http import JsonResponse
from django.shortcuts import render
from django.template.loader import render_to_string
from django.utils.decorators import method_decorator
from django.views.generic import ListView

from medical_history.models import MedicalHistory
from users.decorators import login_required, patient_required
from utils.paginate import paginate


@method_decorator([login_required, patient_required], name='dispatch')
class MedicalHistoryListView(ListView):
    model = MedicalHistory
    template_name = 'medical_history/patient/medical_history.html'
    context_object_name = 'medical_histories'

    def get_queryset(self):
        queryset = MedicalHistory.objects.filter(patient__email=self.request.user).order_by('-date_selected')
        return queryset

    def get(self, request, **kwargs):
        """
        Function override due to adding pagination and search.
        """
        url_without_parameters = str(request.get_full_path()).split('?')[0]
        url_parameter_q = request.GET.get('q')
        if url_parameter_q:
            ctx = {
                'medical_histories': self.get_queryset().filter(owner__office__name__icontains=url_parameter_q),
            }
        else:
            ctx = {
                'medical_histories': self.get_queryset(),
            }
            paginated_medical_histories = paginate(request, ctx['medical_histories'], 10)

            ctx = {
                'medical_histories': paginated_medical_histories,
                'endpoint': url_without_parameters
            }

        if request.is_ajax():
            html = render_to_string(
                template_name='medical_history/patient/medical_history_results_partial.html',
                context=ctx
            )
            data_dict = {"html_from_view": html}
            return JsonResponse(data=data_dict, safe=False)
        return render(request, self.template_name, ctx)
