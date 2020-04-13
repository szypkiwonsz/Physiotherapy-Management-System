from django.contrib.auth.decorators import login_required
from django.db.models import Count
from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect
from django.utils.decorators import method_decorator
from django.views import View
from django.views.generic import ListView

from users.decorators import patient_required, office_required
from users.models import Patient
from users.forms import PatientForm
from django.contrib import messages
from office_panel.views import patient, appointment


class HomeOffice(View):

    template_name = 'office_panel/office_home.html'

    def get(self, request):
        user = request.user
        try:
            if user.is_office:
                pass
        except Exception as e:
            messages.warning(request, 'Nie masz dostępu do tej strony. Zaloguj się jako gabinet.')
            return redirect('login')
        return render(request, self.template_name)


@method_decorator([login_required, office_required], name='dispatch')
class PatientListView(View):
    model = Patient
    ordering = ('owner', )
    template_name = 'office_panel/office_home.html'

    def get_queryset(self):
        queryset = self.request.user.patients \
            .select_related('owner') \
            .annotate(questions_count=Count('first_name', distinct=True)) \
            # .annotate(taken_count=Count('taken_quizzes', distinct=True))
        return queryset[:2]

    def get(self, request):
        context = {
            'patients': patient.PatientListView.get_queryset(self)[:5],
            'appointments': appointment.AppointmentListView.get_queryset(self)[:5]
        }
        return render(request, 'office_panel/office_home.html', context)
