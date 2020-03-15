from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse

from users.forms import OfficeSignUpForm, PatientSignUpForm

from users.multiforms import MultiFormsView


# def form_redir(request):
#     return render(request, 'users/signup_form.html')


def multiple_forms(request):
    if request.method == 'POST':
        office_form = OfficeSignUpForm(request.POST)
        patient_form = PatientSignUpForm(request.POST)
        if office_form.is_valid() or patient_form.is_valid():
            return HttpResponseRedirect(reverse('form-redirect'))
    else:
        office_form = OfficeSignUpForm()
        patient_form = PatientSignUpForm()

    return render(request, 'users/signup_form.html', {
        'office': office_form,
        'patient': patient_form,
    })


class SignUpView(MultiFormsView):
    template_name = "users/signup_form.html"
    form_classes = {'office': OfficeSignUpForm,
                    'patient': PatientSignUpForm,
                    }

    def office_form_valid(self, form):
        email = form.cleaned_data.get('email')
        form_name = form.cleaned_data.get('action')
        return HttpResponseRedirect(self.get_success_url(form_name))

    def patient_form_valid(self, form):
        email = form.cleaned_data.get('email')
        form_name = form.cleaned_data.get('action')
        form = form.save(commit=False)
        form.is_patient = True
        form.save()
        return HttpResponseRedirect(self.get_success_url(form_name))
