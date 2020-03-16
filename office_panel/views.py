from django.shortcuts import render

# Create your views here.
from django.shortcuts import render, redirect
from django.utils.decorators import method_decorator
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required

from users.decorators import office_required

# Create your views here.
@office_required(login_url='login')
def office_home(request):
    return render(request, 'office_panel/office_home.html')