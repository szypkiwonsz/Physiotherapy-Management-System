from django.contrib import messages
from django.contrib.auth import authenticate, login
from django.contrib.auth.forms import AuthenticationForm
from django.shortcuts import redirect, render
from django.utils.decorators import method_decorator
from django.views import View
from django.views.decorators.csrf import csrf_protect

from users.forms import LoginForm

csrf_protected_method = method_decorator(csrf_protect)


class CheckUser(View):

    @staticmethod
    def get(request):
        if request.user.is_authenticated:
            if request.user.is_office:
                return redirect('office-home')
            else:
                return redirect('patient-home')
        else:
            messages.warning(request, "Musisz się zalogować, aby mieć dostęp do tego panelu.")
            return redirect('login')


class LoginView(View):
    form_class = LoginForm
    initial = {'form': 'form'}
    template_name = 'users/login.html'

    def get(self, request):
        form = self.form_class(initial=self.initial)
        return render(request, self.template_name, {'form': form})

    @csrf_protected_method
    def post(self, request):
        if request.method == 'POST':
            form = AuthenticationForm(request=request, data=request.POST)
            if form.is_valid():
                email = form.cleaned_data.get('username')
                password = form.cleaned_data.get('password')
                user = authenticate(email=email, password=password)
                if user is not None:
                    login(request, user)
                    messages.info(request, f"Poprawnie zalogowałeś się.")
                    return redirect('panel')
        else:
            form = AuthenticationForm()
        return render(request, self.template_name, {'form': form})
