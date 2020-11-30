// Script to force the page refresh.
window.onpageshow = function (event) {
    if (event.persisted) {
        window.location.reload();
    }
};