from django.shortcuts import render, redirect
from django.utils.decorators import method_decorator
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required

from users.decorators import patient_required

# Create your views here.
@patient_required(login_url='login')
def patient_home(request):
    return render(request, 'patient_panel/patient_home.html')
