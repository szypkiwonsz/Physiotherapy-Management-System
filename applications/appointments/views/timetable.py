import datetime

from django.http import JsonResponse
from django.shortcuts import render
from django.template.loader import render_to_string
from django.utils.decorators import method_decorator
from django.views.generic import View

from applications.appointments.models import Appointment
from applications.appointments.models import Service
from applications.office_panel.utils import get_number_of_days_in_month, get_dates_in_month, get_dates_taken
from applications.users.decorators import login_required


@method_decorator([login_required], name='dispatch')
class TimetableView(View):
    template_name = 'appointments/timetable.html'

    def get(self, request, pk=None):
        """Function override due to adding month selection."""
        if self.request.user.is_office:
            office_id = self.request.user.useroffice.pk
        else:
            office_id = pk
        now = datetime.date.today()
        # selected year
        url_parameter_y = request.GET.get('y')
        # selected month
        url_parameter_m = request.GET.get('m')
        # selected service
        url_parameter_s = request.GET.get('s')
        if url_parameter_s == 'Wybierz usługę':
            url_parameter_s = None
        if url_parameter_y and url_parameter_m and url_parameter_s:
            service = Service.objects.get(name=url_parameter_s, office=office_id)
            dates_taken = Appointment.objects.filter(
                date__year=int(url_parameter_y), date__month=int(url_parameter_m), office=office_id
            )
            dates = get_dates_in_month(
                office_id=office_id,
                days_in_month=get_number_of_days_in_month(int(url_parameter_y), int(url_parameter_m)),
                month=int(url_parameter_m),
                year=int(url_parameter_y)
            )
            dates_taken = get_dates_taken(dates_taken, service)
            ctx = {
                'dates_taken': dates_taken,
                'year': url_parameter_y,
                'month': url_parameter_m,
                'dates': dates,
                'office_id': office_id,
                'service': service.name,
                'user': self.request.user
            }
        else:
            ctx = {
                'year': now.year,
                'month': now.month,
                'office_id': office_id,
                'services': Service.objects.values_list('name', flat=True).filter(office=office_id)
            }

        if request.is_ajax():
            html = render_to_string(
                template_name='appointments/timetable_results_partial.html',
                context=ctx
            )
            data_dict = {"html_from_view": html}
            return JsonResponse(data=data_dict, safe=False)
        return render(request, self.template_name, ctx)
