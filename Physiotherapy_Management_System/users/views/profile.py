from django.shortcuts import render, redirect
from django.utils.decorators import method_decorator
from django.views import View

from users.decorators import login_required, patient_required, office_required
from users.forms import ProfileUpdateForm, OfficeUpdateForm, UsersUpdateForm, PatientUpdateForm


@method_decorator([login_required, office_required], name='dispatch')
class OfficeProfile(View):
    template_name = 'users/profile.html'

    def get(self, request):
        p_form = ProfileUpdateForm(instance=request.user.profile)
        o_form = OfficeUpdateForm(instance=request.user.office)
        u_form = UsersUpdateForm(instance=request.user)

        context = {
            'o_form': o_form,
            'p_form': p_form,
            'u_form': u_form
        }
        return render(request, self.template_name, context)

    def post(self, request):
        o_form = OfficeUpdateForm(request.POST, instance=request.user.office)
        p_form = ProfileUpdateForm(request.POST, request.FILES, instance=request.user.profile)
        u_form = UsersUpdateForm(request.POST, instance=request.user)

        if p_form.is_valid() and o_form.is_valid() and u_form.is_valid():
            p_form.save()
            o_form.save()
            u_form.save()
            return redirect('users:office_profile')

        context = {
            'p_form': p_form,
            'u_form': u_form,
            'o_form': o_form
        }
        return render(request, self.template_name, context)


@method_decorator([login_required, patient_required], name='dispatch')
class PatientProfile(View):
    template_name = 'users/profile.html'

    def get(self, request):
        p_form = ProfileUpdateForm(instance=request.user.profile)
        o_form = PatientUpdateForm(instance=request.user.userpatient)
        u_form = UsersUpdateForm(instance=request.user)

        context = {
            'o_form': o_form,
            'p_form': p_form,
            'u_form': u_form
        }
        return render(request, self.template_name, context)

    def post(self, request):
        o_form = PatientUpdateForm(request.POST, instance=request.user.userpatient)
        p_form = ProfileUpdateForm(request.POST, request.FILES, instance=request.user.profile)
        u_form = UsersUpdateForm(request.POST, instance=request.user)

        if p_form.is_valid() and o_form.is_valid() and u_form.is_valid():
            p_form.save()
            o_form.save()
            u_form.save()
            return redirect('users:patient_profile')

        context = {
            'p_form': p_form,
            'u_form': u_form,
            'o_form': o_form
        }
        return render(request, self.template_name, context)
