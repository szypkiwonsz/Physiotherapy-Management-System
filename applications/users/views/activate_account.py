from django.contrib import messages
from django.contrib.auth import login
from django.shortcuts import redirect
from django.utils.encoding import force_text
from django.utils.http import urlsafe_base64_decode

from applications.users.models import User
from applications.users.tokens import account_activation_token


def activate(request, uidb64, token):
    """Function that activates the user account."""
    try:
        uid = force_text(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except(TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None
    if user is not None and account_activation_token.check_token(user, token):
        user.is_active = True
        user.save()
        login(request, user)
        messages.success(request, 'Konto zostało pomyślnie aktywowane. Możesz się zalogować.')
        return redirect('login')
    else:
        messages.warning(request, 'Link aktywacyjny jest nieprawidłowy lub konto zostało już aktywowane.')
        return redirect('login')
