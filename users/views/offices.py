from django.views.generic import CreateView
from users.models import User
from users.forms import OfficeSignUpForm


class OfficeSignUpView(CreateView):
    model = User
    form_class = OfficeSignUpForm
    template_name = 'users/signup_form.html'

    def get_context_data(self, **kwargs):
        kwargs['user_type'] = 'office'
        return super().get_context_data(**kwargs)
