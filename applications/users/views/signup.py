from django.contrib import messages
from django.contrib.sites.shortcuts import get_current_site
from django.shortcuts import redirect
from django.views.generic import TemplateView, CreateView

from applications.users.forms import OfficeSignUpForm, PatientSignUpForm
from applications.users.models import Office, UserPatient
from applications.users.tasks import activation_email


def user_save(form, is_patient=False, is_office=False):
    user = form.save(commit=False)
    # The account is not active until the user activates it.
    user.is_active = False
    user.is_patient = is_patient
    user.is_office = is_office
    user.save()
    return user


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
        domain = current_site.domain
        patient_email = form.cleaned_data.get('email')
        activation_email.delay(user.pk, domain, patient_email)
        messages.warning(self.request, 'Potwierdź swoje konto poprzez link wysłany na email.')
        return redirect('login')


class RegisterOffice(CreateView):
    form_class = OfficeSignUpForm
    template_name = 'users/signup_office.html'

    @staticmethod
    def create_office(form, user):
        """Helper function creating a user as a office"""
        office = Office.objects.create(user=user)
        office.name = form.cleaned_data.get('name')
        office.address = form.cleaned_data.get('address')
        office.city = form.cleaned_data.get('city')
        office.phone_number = form.cleaned_data.get('phone_number')
        office.save()

    def form_valid(self, form):
        user = user_save(form, is_office=True)
        self.create_office(form, user)
        current_site = get_current_site(self.request)
        domain = current_site.domain
        office_email = form.cleaned_data.get('email')
        activation_email.delay(user.pk, domain, office_email)
        messages.warning(self.request, 'Potwierdź swoje konto poprzez link wysłany na email.')
        return redirect('login')
