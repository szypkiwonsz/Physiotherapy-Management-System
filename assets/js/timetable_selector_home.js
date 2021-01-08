// Script to correctly display the timetable for the selected month and year.
const service_select = $("#service")
const timetable_div = $('#replaceable-content')
const endpoint = $("#endpoint").attr("value")
const delay_by_in_ms = 0
let scheduled_function = false

let ajax_call = function (endpoint, request_parameters) {
    $.getJSON(endpoint, request_parameters)
        .done(response => {
            // fade out the timetable_div, then:
            timetable_div.fadeTo('slow', 0).promise().then(() => {
                // replace the HTML contents
                timetable_div.html(response['html_from_view'])
                // fade-in the div with new contents
                timetable_div.fadeTo('slow', 1)
            })
        })
}

service_select.change(function() {
      const request_parameters = {
          s: $("#service").val()
    }

    // if scheduled_function is NOT false, cancel the execution of the function
    if (scheduled_function) {
        clearTimeout(scheduled_function)
    }

    // setTimeout returns the ID of the function to be executed
    scheduled_function = setTimeout(ajax_call, delay_by_in_ms, endpoint, request_parameters)
})