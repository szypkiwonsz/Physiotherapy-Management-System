from django.shortcuts import redirect, render
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import authenticate, login
from django.contrib import messages
from django.views import View


def check_user(request):
    if request.user.is_authenticated:
        if request.user.is_office:
            return redirect('office-home')
        else:
            return redirect('patient-home')
    else:
        messages.warning(request, "Musisz się zalogować, aby mieć dostęp do panelu.")
        return redirect('login')


class Login(View):
    form_class = AuthenticationForm
    initial = {'form': 'form'}
    template_name = 'users/login.html'

    def get(self, request):
        form = self.form_class(initial=self.initial)
        return render(request, self.template_name, {'form': form})

    @staticmethod
    def post(request):
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
                    messages.warning(request, "Niepoprawny email lub hasło, bądź twoje konto nie zostało aktywowane.")
            else:
                messages.warning(request, "Niepoprawny email lub hasło, bądź twoje konto nie zostało aktywowane.")
        else:
            form = AuthenticationForm()
        return render(request=request, template_name="users/login.html", context={"form": form})
