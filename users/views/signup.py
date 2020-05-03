from django.contrib.sites.shortcuts import get_current_site
from django.shortcuts import redirect
from django.template.loader import render_to_string
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode
from django.views.generic import TemplateView, CreateView
from django.core.mail import EmailMessage
from django.contrib import messages
from users.models import Office, UserPatient
from users.tokens import account_activation_token
from users.forms import OfficeSignUpForm, PatientSignUpForm


class SignUp:

    @staticmethod
    def send_email(user, current_site, user_email):
        subject = 'Fizjo-System - Aktywacja Konta'
        message = render_to_string('users/activate_email.html', {
            'user': user,
            'domain': current_site.domain,
            'uid': urlsafe_base64_encode(force_bytes(user.pk)),
            'token': account_activation_token.make_token(user),
        })
        to_email = user_email
        email = EmailMessage(
            subject, message, to=[to_email]
        )
        email.send()

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

    def form_valid(self, form):
        user = self.user_save(form, is_patient=True)
        user_patient = UserPatient.objects.create(user=user)
        user_patient.phone_number = form.cleaned_data.get('phone_number')
        user_patient.save()
        current_site = get_current_site(self.request)
        patient_email = form.cleaned_data.get('email')
        self.send_email(user, current_site, patient_email)
        messages.warning(self.request, 'Potwierdź swoje konto poprzez link wysłany na email.')
        return redirect('login')


class RegisterOffice(CreateView, SignUp):
    form_class = OfficeSignUpForm
    template_name = 'users/signup_office.html'

    def form_valid(self, form):
        user = self.user_save(form, is_office=True)
        office = Office.objects.create(user=user)
        office.name = form.cleaned_data.get('name')
        office.address = form.cleaned_data.get('address')
        office.city = form.cleaned_data.get('city')
        office.save()
        current_site = get_current_site(self.request)
        office_email = form.cleaned_data.get('email')
        self.send_email(user, current_site, office_email)
        messages.warning(self.request, 'Potwierdź swoje konto poprzez link wysłany na email.')
        return redirect('login')
