from django.shortcuts import redirect
from django.contrib.auth.views import LoginView
from django.contrib import messages
from django.views import View
from users.forms import LoginForm
from django.views.decorators.csrf import csrf_protect


class CheckUser(View):

    @staticmethod
    def get(request):
        if request.user.is_authenticated:
            if request.user.is_office:
                return redirect('office-home')
            else:
                return redirect('patient-home')
        else:
            messages.warning(request, "Musisz się zalogować, aby mieć dostęp do panelu.")
            return redirect('login')


class Login(LoginView):
    form_class = LoginForm
    initial = {'form': 'form'}
    template_name = 'users/login.html'
