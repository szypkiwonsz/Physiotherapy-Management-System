from django.shortcuts import render
from django.views.generic import TemplateView, View
from users.models import Office


class HomeView(TemplateView):
    template_name = 'home_page/home.html'


class HelpView(TemplateView):
    template_name = 'home_page/help.html'


class Offices(View):
    model = Office
    template_name = 'home_page/offices.html'

    def get(self, request):
        context = {
            'offices': Office.objects.all()
        }
        return render(request, self.template_name, context)
