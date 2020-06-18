from django.contrib import messages
from django.http import HttpResponseRedirect
from django.shortcuts import redirect


def patient_required(function):
    def _function(request, *args, **kwargs):
        if not request.user.is_patient:
            messages.warning(request, 'Aby mieć dostęp do tej sekcji, zaloguj się jako pacjent.')
            return redirect('login')
        return function(request, *args, **kwargs)
    return _function


def office_required(function):
    def _function(request, *args, **kwargs):
        if not request.user.is_office:
            messages.warning(request, 'Aby mieć dostęp do tej sekcji, zaloguj się jako gabinet.')
            return redirect('login')
        return function(request, *args, **kwargs)
    return _function


def login_required(function):
    def _function(request, *args, **kwargs):
        if not request.user.is_authenticated:
            messages.warning(request, 'Aby mieć dostęp do tej sekcji, zaloguj się.')
            return redirect('login')
        return function(request, *args, **kwargs)
    return _function
