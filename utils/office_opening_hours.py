from applications.users.models import OfficeDay


def get_office_opening_hours(office):
    """
    Returns a dictionary with the days of the week as keys and values ​​as the earliest and latest time to make an
    appointment to a given office.

    :param office: <int> -> id of the office
    :return: <dict> -> days of the week with an appointment hour compartment
    """
    days = [OfficeDay.objects.get(office=office, day=i) for i in range(7)]
    opening_hours = {
        'monday': (days[0].earliest_appointment_time, days[0].latest_appointment_time),
        'tuesday': (days[1].earliest_appointment_time, days[1].latest_appointment_time),
        'wednesday': (days[2].earliest_appointment_time, days[2].latest_appointment_time),
        'thursday': (days[3].earliest_appointment_time, days[3].latest_appointment_time),
        'friday': (days[4].earliest_appointment_time, days[4].latest_appointment_time),
        'saturday': (days[5].earliest_appointment_time, days[5].latest_appointment_time),
        'sunday': (days[6].earliest_appointment_time, days[6].latest_appointment_time),
    }
    return opening_hours
