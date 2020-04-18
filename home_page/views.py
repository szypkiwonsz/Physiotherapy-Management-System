from django.views.generic import TemplateView


class HomeView(TemplateView):
    template_name = 'home_page/home.html'
