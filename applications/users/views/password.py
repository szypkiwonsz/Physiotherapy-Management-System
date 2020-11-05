from django.contrib.auth import (get_user_model)
from django.contrib.auth.views import PasswordResetConfirmView

from applications.users.forms import NewSetPasswordForm

UserModel = get_user_model()


class NewPasswordResetConfirmView(PasswordResetConfirmView):
    form_class = NewSetPasswordForm
