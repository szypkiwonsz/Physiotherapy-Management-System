from django.contrib.auth.views import PasswordResetConfirmView

from applications.users.forms import NewSetPasswordForm


class NewPasswordResetConfirmView(PasswordResetConfirmView):
    form_class = NewSetPasswordForm
