var logic = function (currentDateTime) {
    // if selected day is saturday or sunday set time as below.
    if (currentDateTime.getDay() == 6 || currentDateTime.getDay() == 0) {
        this.setOptions({
            minTime: '11:00', maxTime: '14:00'
        });
    } else
        this.setOptions({
            minTime: '16:00', maxTime: '20:00'
        });
};

$('#id_date').keypress(function (e) {
    e.preventDefault();
});
jQuery.datetimepicker.setLocale('pl');
jQuery('#id_date').datetimepicker({
    minDate: '+1970/01/02',//yesterday is minimum date(for today use 0 or -1970/01/01)
    maxDate: '+1970/01/15',//tomorrow is maximum date calendar
    allowTimes: ['11:00',
        '12:00', '13:00', '14:00', '16:00',
        '17:00', '18:00', '19:00'
    ],
    format: 'd.m.Y H:i',
    defaultTime: '00:00',
    onChangeDateTime: logic,
    onShow: logic,
});
