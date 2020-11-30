// Script for a window for selecting the date and time.
var logic = function (currentDateTime) {
    // if selected day is monday set time as below.
    if (currentDateTime.getDay() === 1) {
        this.setOptions({
            minTime: opening_hours.Monday[0], maxTime: opening_hours.Monday[1]
        });
        // if selected day is tuesday set time as below.
    } else if (currentDateTime.getDay() === 2) {
        this.setOptions({
            minTime: opening_hours.Tuesday[0], maxTime: opening_hours.Tuesday[1]
        });
        // if selected day is wednesday set time as below.
    } else if (currentDateTime.getDay() === 3) {
        this.setOptions({
            minTime: opening_hours.Wednesday[0], maxTime: opening_hours.Wednesday[1]
        });
        // if selected day is thursday set time as below.
    } else if (currentDateTime.getDay() === 4) {
        this.setOptions({
            minTime: opening_hours.Thursday[0], maxTime: opening_hours.Thursday[1]
        });
        // if selected day is friday set time as below.
    } else if (currentDateTime.getDay() === 5) {
        this.setOptions({
            minTime: opening_hours.Friday[0], maxTime: opening_hours.Friday[1]
        });
        // if selected day is saturday set time as below.
    } else if (currentDateTime.getDay() === 6) {
        this.setOptions({
            minTime: opening_hours.Saturday[0], maxTime: opening_hours.Saturday[1]
        });
        // if selected day is sunday set time as below.
    } else
        this.setOptions({
            minTime: opening_hours.Sunday[0], maxTime: opening_hours.Sunday[1]
        });
};

$('#id_date').keypress(function (e) {
    e.preventDefault();
});

jQuery.datetimepicker.setLocale('pl');
jQuery('#id_date').datetimepicker({
    minDate: '+1970/01/02', // yesterday is minimum date(for today use 0 or -1970/01/01)
    maxDate: '+1970/01/15', // tomorrow is maximum date calendar
    allowTimes: [
        '00:00', '01:00', '02:00', '03:00', '04:00', '05:00', '06:00', '07:00', '08:00', '09:00', '10:00', '11:00',
        '12:00', '13:00', '14:00', '15:00', '16:00', '17:00', '18:00', '19:00', '20:00', '21:00', '22:00', '23:00'
    ],
    format: 'd.m.Y H:i',
    defaultTime: '23:59',
    onChangeDateTime: logic,
    onShow: logic,
});
