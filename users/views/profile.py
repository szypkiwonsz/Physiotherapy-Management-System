from django.shortcuts import render, redirect
from django.views import View
from users.forms import ProfileUpdateForm


class Profile(View):
    template_name = 'users/profile.html'

    def get(self, request):
        p_form = ProfileUpdateForm(instance=request.user.profile)

        context = {
            'p_form': p_form
        }
        return render(request, self.template_name, context)

    def post(self, request):
        p_form = ProfileUpdateForm(request.POST, request.FILES, instance=request.user.profile)

        if p_form.is_valid():
            p_form.save()
            return redirect('profile')

        context = {
            'p_form': p_form
        }
        return render(request, self.template_name, context)
