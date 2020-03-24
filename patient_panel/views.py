from django.shortcuts import render
from users.models import Office

from users.decorators import patient_required

# Create your views here.
@patient_required(login_url='login')
def patient_home(request):
    author = request.user

    context = {
        'offices': Office.objects.filter(user__patients__email=author),
    }
    return render(request, 'patient_panel/patient_home.html', context)
