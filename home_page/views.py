from django.shortcuts import render
from django.views.generic import TemplateView, ListView

from users.models import Office


class HomeView(TemplateView):
    template_name = 'home_page/home.html'


class HelpView(TemplateView):
    template_name = 'home_page/help.html'


class OfficesView(ListView):
    model = Office
    template_name = 'home_page/offices.html'
    context_object_name = 'offices'
