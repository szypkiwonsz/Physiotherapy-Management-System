from django.shortcuts import render
from django.views import View


class Profile(View):
    template_name = 'users/profile.html'

    def get(self, request):
        return render(request, self.template_name)
