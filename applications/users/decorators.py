from django.contrib import messages
from django.shortcuts import redirect


def patient_required(function):
    """Decorator checking if the user is logged in as an patient."""

    def _function(request, *args, **kwargs):
        if not request.user.is_patient:
            messages.warning(request, 'Aby mieć dostęp do tej sekcji, zaloguj się jako pacjent.')
            return redirect('login')
        return function(request, *args, **kwargs)

    return _function


def office_required(function):
    """Decorator checking if the user is logged in as an office."""

    def _function(request, *args, **kwargs):
        if not request.user.is_office:
            messages.warning(request, 'Aby mieć dostęp do tej sekcji, zaloguj się jako gabinet.')
            return redirect('login')
        return function(request, *args, **kwargs)

    return _function


def login_required(function):
    """Decorator checking if the user is logged in."""

    def _function(request, *args, **kwargs):
        if not request.user.is_authenticated:
            messages.warning(request, 'Aby mieć dostęp do tej sekcji, zaloguj się.')
            return redirect('login')
        return function(request, *args, **kwargs)

    return _function
