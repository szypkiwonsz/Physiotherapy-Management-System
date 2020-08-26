from django.http import JsonResponse
from django.shortcuts import render
from django.template.loader import render_to_string
from django.utils.decorators import method_decorator
from django.views import View

from users.decorators import login_required, patient_required
from users.models import Office
from utils.paginate import paginate


@method_decorator([login_required, patient_required], name='dispatch')
class OfficesListView(View):
    model = Office
    template_name = 'patient_panel/offices.html'

    def get_queryset(self):
        queryset = Office.objects.filter(user__patients__email=self.request.user)
        return queryset

    def get(self, request):
        url_without_parameters = str(request.get_full_path()).split('?')[0]
        url_parameter_q = request.GET.get('q')
        if url_parameter_q:
            ctx = {
                'offices': self.get_queryset().filter(name__icontains=url_parameter_q)
            }
        else:
            ctx = {
                'offices': self.get_queryset(),
            }
            paginated_offices = paginate(request, ctx['offices'], 10)

            ctx = {
                'offices': paginated_offices,
                'endpoint': url_without_parameters
            }

        if request.is_ajax():
            html = render_to_string(
                template_name='patient_panel/offices_results_partial.html',
                context=ctx
            )
            data_dict = {"html_from_view": html}
            return JsonResponse(data=data_dict, safe=False)
        return render(request, self.template_name, ctx)
