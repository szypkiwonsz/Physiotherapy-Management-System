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
        'monday': (days[0].earliest_appointment_time,
                   str(int(days[0].latest_appointment_time.split(':')[0]) + 1) + ':00'),
        'tuesday': (days[1].earliest_appointment_time,
                    str(int(days[1].latest_appointment_time.split(':')[0]) + 1) + ':00'),
        'wednesday': (days[2].earliest_appointment_time,
                      str(int(days[2].latest_appointment_time.split(':')[0]) + 1) + ':00'),
        'thursday': (days[3].earliest_appointment_time,
                     str(int(days[3].latest_appointment_time.split(':')[0]) + 1) + ':00'),
        'friday': (days[4].earliest_appointment_time,
                   str(int(days[4].latest_appointment_time.split(':')[0]) + 1) + ':00'),
        'saturday': (days[5].earliest_appointment_time,
                     str(int(days[5].latest_appointment_time.split(':')[0]) + 1) + ':00'),
        'sunday': (days[6].earliest_appointment_time,
                   str(int(days[6].latest_appointment_time.split(':')[0]) + 1) + ':00'),
    }
    return opening_hours
