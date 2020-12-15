from django.views.generic import TemplateView, ListView

from applications.users.models import UserOffice


class HomeView(TemplateView):
    template_name = 'home_page/home.html'


class HelpView(TemplateView):
    template_name = 'home_page/help.html'


class OfficesView(ListView):
    model = UserOffice
    template_name = 'home_page/offices.html'
    context_object_name = 'offices'
