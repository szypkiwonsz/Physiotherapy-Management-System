from django.contrib.sites.shortcuts import get_current_site
from django.shortcuts import redirect
from django.views.generic import TemplateView, CreateView
from django.contrib import messages
from users.models import Office, UserPatient
from users.forms import OfficeSignUpForm, PatientSignUpForm
from utils.send_email import activation_email


class SignUp:

    @staticmethod
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


class RegisterPatient(CreateView, SignUp):
    form_class = PatientSignUpForm
    template_name = 'users/signup_patient.html'

    @staticmethod
    def create_patient(form, user):
        user_patient = UserPatient.objects.create(user=user)
        user_patient.phone_number = form.cleaned_data.get('phone_number')
        user_patient.save()

    def form_valid(self, form):
        user = self.user_save(form, is_patient=True)
        self.create_patient(form, user)
        current_site = get_current_site(self.request)
        patient_email = form.cleaned_data.get('email')
        activation_email(user, current_site, patient_email)
        messages.warning(self.request, 'Potwierdź swoje konto poprzez link wysłany na email.')
        return redirect('login')


class RegisterOffice(CreateView, SignUp):
    form_class = OfficeSignUpForm
    template_name = 'users/signup_office.html'

    @staticmethod
    def create_office(form, user):
        office = Office.objects.create(user=user)
        office.name = form.cleaned_data.get('name')
        office.address = form.cleaned_data.get('address')
        office.city = form.cleaned_data.get('city')
        office.save()

    def form_valid(self, form):
        user = self.user_save(form, is_office=True)
        self.create_office(form, user)
        current_site = get_current_site(self.request)
        office_email = form.cleaned_data.get('email')
        activation_email(user, current_site, office_email)
        messages.warning(self.request, 'Potwierdź swoje konto poprzez link wysłany na email.')
        return redirect('login')
