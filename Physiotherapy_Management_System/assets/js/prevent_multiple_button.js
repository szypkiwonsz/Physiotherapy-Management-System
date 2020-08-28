$('form').submit(function () {
    $(this).find(':submit').attr('disabled', 'disabled');
});