from django.shortcuts import render, redirect
from django.views import View
from users.forms import ProfileUpdateForm, OfficeUpdateForm, UsersUpdateForm


class Profile(View):
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
            return redirect('profile')

        context = {
            'p_form': p_form,
            'u_form': u_form,
            'o_form': o_form
        }
        return render(request, self.template_name, context)
