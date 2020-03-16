from django.shortcuts import render, redirect
from django.contrib import messages
from .forms import AppointmentForm, AppointmentCancel
from .models import Appointment
from django.contrib.auth.models import User
from .methods import DateTime
from django.core.mail import EmailMessage
from django.contrib.auth.decorators import login_required


# Create your views here.
@login_required(login_url='login')
def make_appointment(request):
    admin_email = 'kacpersawicki321@gmail.com'

    if request.method == 'POST':

        form = AppointmentForm(request.POST)
        if form.is_valid():
            date = form.cleaned_data.get('date')
            name = form.cleaned_data.get('name')

            if date.hour == 0:
                messages.warning(request, f'Please select the correct time.')
                return redirect('appointments-make_appointment')

            # Checks if first name is typed correctly without any numbers etc.
            elif name.isalpha() is not True:
                messages.warning(request, f'Incorrect name.')
                return redirect('appointments-make_appointment')

            else:
                data = Appointment.objects.raw('select * FROM appointments_appointment')
                for i in data:
                    if date == i.date:
                        messages.warning(request, f'Selected date is already taken.')
                        return redirect('appointments-make_appointment')
                form = form.save(commit=False)
                author = request.user
                form.author = author
                form.save()
                subject = 'Appointment - {}'.format(admin_email)
                message = '''{} was appointed for {}:{} on day {}.{}.{}.
                              Confirm the visit in the admin panel.'''.format(name,
                                                                                            DateTime.add_zero(
                                                                                                date.hour),
                                                                                            DateTime.add_zero(
                                                                                                date.minute),
                                                                                            DateTime.add_zero(date.day),
                                                                                            DateTime.add_zero(
                                                                                                date.month),
                                                                                            DateTime.add_zero(
                                                                                                date.year))
                email = EmailMessage(subject, message, to=[admin_email])
                email.send()

                author_email = User.objects.filter(is_active=True).values_list('email', flat=True)
                subject = 'Your appointments on fizjo-med has been correctly arranged'
                message = 'You have been correctly arranged to visit for {}:{} on day {}.{}.{}. ' \
                          'If you want to cancel your visit, use the form on our website.'.format(
                            DateTime.add_zero(date.hour),
                            DateTime.add_zero(date.minute),
                            DateTime.add_zero(date.day),
                            DateTime.add_zero(date.month),
                            DateTime.add_zero(date.year))
                email = EmailMessage(subject, message, to=[admin_email])
                email.send()
                messages.warning(request, f'You have made an appointments correctly. But you have to wait for confirmation. ')
                return redirect('appointments-make_appointment')
    else:
        form = AppointmentForm()
    return render(request, 'appointment/make_appointment.html', {'form': form})


@login_required(login_url='login')
def cancel_appointment(request):
    if request.method == 'POST':
        form = AppointmentCancel(request.POST)
        if form.is_valid():
            key = form.cleaned_data.get('key')
            data = Appointment.objects.raw('select * FROM appointments_appointment')
            for i in data:
                if key == i.key:
                    Appointment.objects.filter(key=key).delete()
                    messages.success(request, f'You have successfully canceled your visit.')
                    return redirect('appointments-make_appointment')
            messages.warning(request, f'Incorrect key.')
            return redirect('appointments-cancel_appointment')
    else:
        form = AppointmentCancel()
    return render(request, 'appointment/confirm_cancel_appointment.html', {'form': form})



