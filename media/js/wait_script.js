/**
 * Created by wardcoessens on 21/04/14.
 */
var timer, order_path;

function orderDone() {
    // Toggle visible icon ( from waiting to done )
    $('#wait-for-order-icon').attr('hidden', '');
    $('#done-order-icon').removeAttr('hidden');

    // Change text
    $('#wait-for-order-title').text("");
    $('#wait-for-order-bottom').html("Uw bestelling is klaar <br> om af te halen aan de bar!");

    // Changing title
    $(document).attr('title', 'bestelling klaar');

    // Popup
    alert("Bestelling klaar!");
}

function orderCancelled() {
    // Toggle visible icon ( from waiting to done )
    $('#wait-for-order-icon').attr('hidden', '');
    $('#cancelled-order-icon').removeAttr('hidden');

    // Change text
    $('#wait-for-order-title').text("");
    $('#wait-for-order-bottom').html("Uw bestelling is geweigerd <br> ga naar de bar voor meer info");

    // Changing title
    $(document).attr('title', 'bestelling geweigerd');

    // Popup
    alert("Bestelling werd geweigerd");
}

function refresh() {
    $.ajax({
        url: order_path,
        context: document.body,
        dataType: "json"
    }).done(function (data) {
        window.clearInterval(timer);
        if (data.status == 'DO') {
            orderDone();
        } else if (data.status == 'CA') {
            orderCancelled();
        } else if (data.next_check_timeout) {
            timer = window.setInterval(refresh, data.next_check_timeout);
        }
    })
}

$(function () {
    $('#done-order-icon').attr('hidden', '');
    order_path = "/wait_status/" + $('#order_uuid').text() + "/";
    refresh();
});
