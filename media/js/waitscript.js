/**
 * Created with PyCharm.
 * User: ward
 * Date: 8/17/13
 * Time: 1:30 PM
 * To change this template use File | Settings | File Templates.
 */

function refresh(){
    $.ajax({
        url: order_path,
        context: document.body,
        dataType: "json"
    }).done(function(data){
        $(this).find("#waitstate").text(data.state)
    })
}

$(document).ready(function () {
    order_path = window.location.pathname
    window.setInterval(refresh, 2000);
})
