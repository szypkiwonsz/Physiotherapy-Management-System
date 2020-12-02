// Script to block a button after a single click.
$('form').submit(function () {
    $(this).find(':submit').attr('disabled', 'disabled');
});