from django.shortcuts import render
from django.utils.decorators import method_decorator
from django.views import View

from users.decorators import login_required, patient_required
from users.models import Office


@method_decorator([login_required, patient_required], name='dispatch')
class OfficesListView(View):
    model = Office
    template_name = 'patient_panel/patient_office.html'

    def get_queryset(self):
        queryset = Office.objects.filter(user__patients__email=self.request.user)
        return queryset

    def get(self, request):
        context = {
            'offices': self.get_queryset(),
        }
        return render(request, 'patient_panel/patient_office.html', context)
