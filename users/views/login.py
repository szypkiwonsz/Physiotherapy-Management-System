from django.shortcuts import redirect



def check_user(request):
    if request.user.is_authenticated:
        if request.user.is_office:
            return redirect('office-home')
        else:
            return redirect('patient-home')
    else:
        return redirect('login')
