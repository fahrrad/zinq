/**
 * Created by wardcoessens on 21/04/14.
 */
var timer, order_path

function refresh(){
    $.ajax({
        url: order_path,
        context: document.body,
        dataType: "json"
    }).done(function(data){
        if(data.status_done){
            window.clearInterval(timer)
            $('#wait-for-order-icon').attr('hidden','');
            $('#done-order-icon').removeAttr('hidden');
            alert("Done!")
        }else{
            $(this).find("#waitstate").text(data.status_display);
            window.clearInterval(timer);
            if (data.check_next)
                window.clearInterval(timer)
                timer = window.setInterval(refresh, data.next_check_timeout)
            }
    })
}

order_path = "/wait/" + $('#order_uuid').text();
timer = window.setInterval(refresh, 2000);