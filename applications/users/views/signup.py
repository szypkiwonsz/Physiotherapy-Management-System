from django.contrib import messages
from django.contrib.sites.shortcuts import get_current_site
from django.shortcuts import redirect
from django.views.generic import TemplateView, CreateView

from applications.users.forms import OfficeSignUpForm, PatientSignUpForm
from applications.users.models import UserOffice, UserPatient
from applications.users.tasks import send_activation_email
from applications.users.utils import user_save


class Register(TemplateView):
    template_name = 'users/signup.html'


class RegisterPatient(CreateView):
    form_class = PatientSignUpForm
    template_name = 'users/signup_patient.html'

    @staticmethod
    def create_patient(form, user):
        """Helper function creating a user as a patient"""
        user_patient = UserPatient.objects.create(user=user)
        user_patient.phone_number = form.cleaned_data.get('phone_number')
        user_patient.save()

    def form_valid(self, form):
        user = user_save(form, is_patient=True)
        self.create_patient(form, user)
        current_site = get_current_site(self.request)
        send_activation_email.delay(
            user_id=user.pk, domain=current_site.domain, user_email=form.cleaned_data.get('email')
        )
        messages.warning(self.request, 'Potwierdź swoje konto poprzez link wysłany na email.')
        return redirect('login')


class RegisterOffice(CreateView):
    form_class = OfficeSignUpForm
    template_name = 'users/signup_office.html'

    @staticmethod
    def create_office(form, user):
        """Helper function creating a user as a office"""
        office = UserOffice.objects.create(user=user)
        office.name = form.cleaned_data.get('name')
        office.address = form.cleaned_data.get('address')
        office.city = form.cleaned_data.get('city')
        office.phone_number = form.cleaned_data.get('phone_number')
        office.save()

    def form_valid(self, form):
        user = user_save(form, is_office=True)
        self.create_office(form, user)
        current_site = get_current_site(self.request)
        send_activation_email.delay(
            user_id=user.pk, domain=current_site.domain, user_email=form.cleaned_data.get('email')
        )
        messages.warning(self.request, 'Potwierdź swoje konto poprzez link wysłany na email.')
        return redirect('login')
