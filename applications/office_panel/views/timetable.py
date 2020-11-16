import datetime

from django.http import JsonResponse
from django.shortcuts import render
from django.template.loader import render_to_string
from django.utils.decorators import method_decorator
from django.views.generic import View

from applications.appointments.models import Appointment
from applications.office_panel.utils import get_number_of_days_in_month, get_hours_in_day
from applications.users.decorators import login_required, office_required
from utils.add_zero import add_zero


@method_decorator([login_required, office_required], name='dispatch')
class TimetableView(View):
    template_name = 'office_panel/timetable/timetable.html'
    hour_open = 11
    hour_close = 20

    @staticmethod
    def get_dates_in_month(days_in_month, hours_in_day, month, year):
        dates = []
        for day in days_in_month:
            day = add_zero(day)
            for hour in hours_in_day:
                date = f'{day}.{month}.{year} {hour}'
                dates.append(date)
        return dates

    def get(self, request):
        """
        Function override due to adding month selection.
        """
        url_without_parameters = str(request.get_full_path()).split('?')[0]
        url_parameter_y = request.GET.get('y')
        url_parameter_m = request.GET.get('m')
        request.session['hour_open'] = add_zero(self.hour_open)
        request.session['hour_close'] = add_zero(self.hour_close)
        if url_parameter_y and url_parameter_m:
            dates_taken = Appointment.objects.filter(
                date__year=int(url_parameter_y), date__month=int(url_parameter_m), office__user=request.user
            )
            dates = self.get_dates_in_month(
                days_in_month=get_number_of_days_in_month(int(url_parameter_y), int(url_parameter_m)),
                hours_in_day=get_hours_in_day(self.hour_open, self.hour_close),
                month=int(url_parameter_m),
                year=int(url_parameter_y)
            )
            ctx = {
                'dates_taken': [str(x.date.strftime('%d.%m.%Y %H:%M')) for x in dates_taken],
                'year': url_parameter_y,
                'month': url_parameter_m,
                'dates': dates,
                'hours': get_hours_in_day(self.hour_open, self.hour_close),
                'days': get_number_of_days_in_month(int(url_parameter_y), int(url_parameter_m)),
                'endpoint': url_without_parameters,
                'office_id': self.request.user.pk
            }
        else:
            now = datetime.datetime.now()
            dates_taken = Appointment.objects.filter(
                date__year=now.year, date__month=now.month, office__user=request.user
            )
            dates = self.get_dates_in_month(
                days_in_month=get_number_of_days_in_month(now.year, now.month),
                hours_in_day=get_hours_in_day(self.hour_open, self.hour_close),
                month=now.month,
                year=now.year
            )
            ctx = {
                'dates_taken': [str(x.date.strftime('%d.%m.%Y %H:%M')) for x in dates_taken],
                'year': now.year,
                'month': now.month,
                'dates': dates,
                'hours': get_hours_in_day(self.hour_open, self.hour_close),
                'days': get_number_of_days_in_month(now.year, now.month),
                'endpoint': url_without_parameters,
                'office_id': self.request.user.pk
            }

        if request.is_ajax():
            html = render_to_string(
                template_name='office_panel/timetable/timetable_results_partial.html',
                context=ctx
            )
            data_dict = {"html_from_view": html}
            return JsonResponse(data=data_dict, safe=False)
        return render(request, self.template_name, ctx)
