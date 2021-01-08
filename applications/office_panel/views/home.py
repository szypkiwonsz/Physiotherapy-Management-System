import datetime

from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.shortcuts import render
from django.template.loader import render_to_string
from django.utils.decorators import method_decorator
from django.views import View

from applications.appointments.models import Appointment, Service
from applications.medical_history.models import MedicalHistory
from applications.office_panel.models import Patient
from applications.office_panel.utils import get_number_of_days_in_month, get_dates_in_month, get_dates_taken
from applications.users.decorators import office_required


@method_decorator([login_required, office_required], name='dispatch')
class OfficePanelView(View):
    model = Patient
    template_name = 'office_panel/home.html'

    @staticmethod
    def get_next_available_dates(all_dates, dates_taken, tomorrow):
        """Returns a list of upcoming appointments dates that can be arranged (from tomorrow)."""
        result_dates = []
        for dates in all_dates:
            list_of_dates = []
            for date in dates:
                # display dates only from tomorrow and if date is not taken by another patient
                if datetime.datetime.strptime(date, '%d.%m.%Y %H:%M') > tomorrow and date not in dates_taken:
                    list_of_dates.append(date)
            if list_of_dates:
                result_dates.append(list_of_dates)
        return result_dates

    def get(self, request):
        now = datetime.datetime.now()

        days = get_number_of_days_in_month(now.year, now.month)
        dates = get_dates_in_month(office_id=self.request.user.useroffice.pk, days_in_month=days, month=now.month,
                                   year=now.year)
        dates_taken = Appointment.objects.filter(date__gte=now, office__user=request.user)
        all_dates = dates
        url_parameter_s = request.GET.get('s')
        if url_parameter_s == 'Wybierz usługę':
            url_parameter_s = None
        if url_parameter_s:
            service = Service.objects.get(name=url_parameter_s, office=self.request.user.useroffice)
            dates_taken = get_dates_taken(dates_taken, service)
            result_dates = self.get_next_available_dates(all_dates, dates_taken, now)
        else:
            service = None
            result_dates = None

        ctx = {
            'services': Service.objects.values_list('name', flat=True).filter(office=request.user.useroffice),
            'service': service,
            'patients': Patient.objects.filter(owner=self.request.user.id).order_by('-date_selected')[:5],
            'dates': result_dates,
            'appointments': Appointment.objects.filter(office=self.request.user.id).order_by('date')[:5],
            'medical_histories': MedicalHistory.objects.filter(owner=self.request.user.id).order_by(
                '-date_selected')[:5],
            'office_id': self.request.user.pk
        }
        if request.is_ajax():
            html = render_to_string(
                template_name='office_panel/home_timetable_results_partial.html',
                context=ctx
            )
            data_dict = {"html_from_view": html}
            return JsonResponse(data=data_dict, safe=False)
        return render(request, self.template_name, ctx)
