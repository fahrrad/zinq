/**
 * Created with PyCharm.
 * User: ward
 * Date: 8/17/13
 * Time: 1:30 PM
 * To change this template use File | Settings | File Templates.
 */
var timer, order_path

function refresh(){
    $.ajax({
        url: order_path,
        context: document.body,
        dataType: "json"
    }).done(function(data){
        $(this).find("#waitstate").text(data.status_display);
        window.clearInterval(timer);
        if (data.check_next)
            timer = window.setInterval(refresh, data.next_check_timeout)
    })
}


$(document).ready(function () {
    order_path = window.location.pathname;
    timer = window.setInterval(refresh, 2000);
})
