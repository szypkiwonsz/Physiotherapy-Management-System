// Script to correctly display the timetable for the selected month and year.
const date_select_up = $("#date-select-up")
const date_select_down = $("#date-select-down")
const service_select = $("#service")
const timetable_div = $('#replaceable-content')
const endpoint = $("#endpoint").attr("value")
const delay_by_in_ms = 0
let scheduled_function = false
let today = new Date();
let yyyy = today.getFullYear()
let mm = today.getMonth() + 1;

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


date_select_up.click(function () {
    if (mm < 12){
        mm += 1
    }
    else {
        yyyy +=1
        mm = 1
    }

    const request_parameters = {
        m: mm, // currently viewed month
        y: yyyy, // currently viewed year
        s: $("#service").val()
    }

    // if scheduled_function is NOT false, cancel the execution of the function
    if (scheduled_function) {
        clearTimeout(scheduled_function)
    }

    // setTimeout returns the ID of the function to be executed
    scheduled_function = setTimeout(ajax_call, delay_by_in_ms, endpoint, request_parameters)
})

date_select_down.click(function () {
    if (mm > 1){
        mm -= 1
    }
    else {
        yyyy -=1
        mm = 12
    }

    const request_parameters = {
        m: mm, // value of user_input: the HTML element with ID user-input
        y: yyyy,
        s: $("#service").val()
    }

    // if scheduled_function is NOT false, cancel the execution of the function
    if (scheduled_function) {
        clearTimeout(scheduled_function)
    }

    // setTimeout returns the ID of the function to be executed
    scheduled_function = setTimeout(ajax_call, delay_by_in_ms, endpoint, request_parameters)
})

service_select.change(function() {
      const request_parameters = {
        m: mm, // value of user_input: the HTML element with ID user-input
        y: yyyy,
          s: $("#service").val()
    }

    // if scheduled_function is NOT false, cancel the execution of the function
    if (scheduled_function) {
        clearTimeout(scheduled_function)
    }

    // setTimeout returns the ID of the function to be executed
    scheduled_function = setTimeout(ajax_call, delay_by_in_ms, endpoint, request_parameters)
})