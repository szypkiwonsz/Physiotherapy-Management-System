from django.shortcuts import redirect
from .forms import MedicalHistoryForm

# Create your views here.
from django.views.generic import CreateView


class MakeMedicalHistory(CreateView):
    form_class = MedicalHistoryForm
    context_object_name = 'medicalhistory'
    template_name = 'medical_history/add_medical_history.html'

    def form_valid(self, form):
        post = form.save(commit=False)
        post.owner_id = self.request.user.id
        post.save()
        return redirect('office-patients')