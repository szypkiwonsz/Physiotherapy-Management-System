from django.contrib.sites.shortcuts import get_current_site
from django.shortcuts import render, redirect
from django.template.loader import render_to_string
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode
from users.tokens import account_activation_token
from django.core.mail import EmailMessage
from django.contrib import messages
from django.views import View
from users.models import Office
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
    def email_valid(form):
        email = form.cleaned_data.get('email')
        confirm_email = form.cleaned_data.get('confirm_email')
        if email != confirm_email:
            return False

    @staticmethod
    def user_save(form, is_patient=False, is_office=False):
        user = form.save(commit=False)
        # The account is not active until the user activates it.
        user.is_active = False
        user.is_patient = is_patient
        user.is_office = is_office
        user.save()
        return user


class RegisterPatient(View, SignUp):
    form_class = PatientSignUpForm
    initial = {'form': 'form'}
    template_name = 'users/signup_patient.html'

    def get(self, request):
        form = self.form_class(initial=self.initial)
        return render(request, self.template_name, {'form': form})

    def post(self, request):
        form = PatientSignUpForm(request.POST)
        if form.is_valid():
            user = self.user_save(form, is_patient=True)
            current_site = get_current_site(request)
            patient_email = form.cleaned_data.get('email')
            self.send_email(user, current_site, patient_email)
            messages.warning(request, 'Potwierdź swoje konto poprzez link wysłany na email.')
            return redirect('login')

        return render(request, self.template_name, {'form': form})


class RegisterOffice(View, SignUp):
    form_class = OfficeSignUpForm
    initial = {'form': 'form'}
    template_name = 'users/signup_office.html'

    def get(self, request):
        form = self.form_class(initial=self.initial)
        return render(request, self.template_name, {'form': form})

    def post(self, request):
        form = OfficeSignUpForm(request.POST)
        if form.is_valid():
            user = self.user_save(form, is_office=True)
            office = Office.objects.create(user=user)
            office.name = form.cleaned_data.get('name')
            office.save()
            current_site = get_current_site(request)
            office_email = form.cleaned_data.get('email')
            self.send_email(user, current_site, office_email)
            messages.warning(request, 'Potwierdź swoje konto poprzez link wysłany na email.')
            return redirect('login')

        return render(request, self.template_name, {'form': form})
