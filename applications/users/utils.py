import calendar

from utils.add_zero import add_zero


def get_days_of_week():
    """A function that returns a list of the names of the days of the week."""
    day_name = ['Poniedziałek', 'Wtorek', 'Środa', 'Czwartek', 'Piątek', 'Sobota', 'Niedziela']
    return [(str(i), (day_name[i]).capitalize()) for i in range(7)]


def get_hours_in_day():
    """A function that returns a list of hours in day."""
    return [(f'{add_zero(i)}:00', f'{add_zero(i)}:00') for i in range(24)]


def user_save(form, is_patient=False, is_office=False):
    """Function saving the user to the database."""
    user = form.save(commit=False)
    # The account is not active until the user activates it.
    user.is_active = False
    user.is_patient = is_patient
    user.is_office = is_office
    user.save()
    return user
