import datetime

from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from django.utils.decorators import method_decorator
from django.views import View

from applications.appointments.models import Appointment
from applications.medical_history.models import MedicalHistory
from applications.office_panel.models import Patient
from applications.office_panel.utils import get_number_of_days_in_month, get_hours_in_day
from applications.users.decorators import office_required
from utils.add_zero import add_zero


@method_decorator([login_required, office_required], name='dispatch')
class OfficePanelView(View):
    model = Patient
    template_name = 'office_panel/home.html'

    def get(self, request):
        now = datetime.datetime.now()
        yesterday = datetime.datetime(now.year, now.month, now.day - 1)
        tomorrow = datetime.datetime(now.year, now.month, now.day + 1)

        days = get_number_of_days_in_month(now.year, now.month)
        dates = get_dates_in_month(request=request, days_in_month=days, month=now.month, year=now.year)
        taken_dates = Appointment.objects.filter(
            date__gte=yesterday, office__user=request.user
        )
        all_dates = dates
        taken_dates = [str(x.date.strftime('%d.%m.%Y %H:%M')) for x in taken_dates]
        final_dates = []
        for dates in all_dates:
            list_of_dates = []
            for date in dates:
                if datetime.datetime.strptime(date, '%d.%m.%Y %H:%M') > now and date not in taken_dates:
                    list_of_dates.append(date)
            if list_of_dates:
                final_dates.append(list_of_dates)

        context = {
            'patients': Patient.objects.filter(owner=self.request.user.id).order_by('-date_selected')[:5],
            'dates': final_dates,
            'hours': hours_in_day,
            'appointments': Appointment.objects.filter(office=self.request.user.id).order_by('date')[:5],
            'medical_histories': MedicalHistory.objects.filter(owner=self.request.user.id).order_by(
                '-date_selected')[:5],
            'office_id': self.request.user.pk
        }
        return render(request, self.template_name, context)
