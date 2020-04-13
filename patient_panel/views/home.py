from django.db.models import Count
from django.shortcuts import render
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from django.views import View
from users.models import Office
from users.decorators import patient_required


@method_decorator([login_required, patient_required], name='dispatch')
class PatientHome(View):
    ordering = ('owner', )
    template_name = 'patient_panel/patient_home.html'

    def get_queryset(self):
        queryset = self.request.user.appointments \
            .select_related('owner') \
            .annotate(questions_count=Count('owner', distinct=True)) \
            # .annotate(taken_count=Count('taken_quizzes', distinct=True))
        return queryset

    def get(self, request):
        context = {
            'offices': Office.objects.filter(user__patients__email=self.request.user)[:5],
            'appointments': self.get_queryset()[:5]
        }
        return render(request, 'patient_panel/patient_home.html', context)


