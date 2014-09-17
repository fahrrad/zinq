var debug = 0;

function log(text) {
    if (debug && window.console && window.console.log) {
        console.log(text);
    }
}

function time_tick() {
    log("Time tick!");

    $(".order-line-wrapper").each(function () {
            $(this).data("seconds",
                    $(this).data("seconds") + 1);
            $(this).find(".time").html(
                seconds_to_minutes($(this).data("seconds")));
//            $(this).css("background-color",
//                seconds_to_color(
//                    $(this).data("seconds")));
        }
    )
}

function paddy(n, p, c) {
    var pad_char = typeof c === 'undefined' ? '0' : c;
    var pad = new Array(1 + p).join(pad_char);
    return (pad + n).slice(-pad.length);
}

function seconds_to_minutes(seconds){
    var minutes = Math.floor(seconds / 60);
    minutes += ':';
    var secs = (seconds % 60);
    minutes += paddy(secs, 2);

    return minutes;
}

function seconds_to_color(seconds){
    //var color = "hsla(" +seconds % 360 +", " +(seconds * 3) % 100 +"%, " +"100%, " +"1.0)";
    var color = "rgb(" + Math.min(255,(seconds * 7) ) + ",0,0)";
    log(color);

    return color;
}

function barsclick () {
    var order_line_wrapper = $(this).closest(".order-line-wrapper");

    // Hide all expanded except this one
    $(".order-line.expanded").slideUp();
    $(order_line_wrapper).find(".expanded").slideDown();

    // disable this button, to avoid opening and closing of an open orderitem
    $("img.3bars").off("click");
    $("img.3bars").click(barsclick);
    $(order_line_wrapper).find("img.3bars").off("click");
}



$("button.cancel_button").click(function () {
    log("cancel order");
});


$("button.ready_button").click(function () {
    var wrapper = $(this).closest(".order-line-wrapper");
    var order_uuid = $(wrapper).data("uuid");
    $.ajax({
        url: "/orders/d/" + order_uuid + "/",
        type: "GET"
    }).done(function () {
        wrapper.slideUp(400, function () {
            wrapper.remove();
        });

    }).error(function () {
        log("Something went south...");
    });
});

function fetchData()
{
    var template = $('#template').clone(),
        item_template = $('.order-item', template).clone();

    template.show();
    template.removeAttr('id');
    $('.table', template).html('99');
    $('.total-amount', template).html('€ 33,76');
    template.data('seconds', 20);
    template.data('uuid', 'lalaland');
    $('.order-item-wrapper', template).html('');

    for(var i=1;i<5;i++) {

        console.log(i);
        $('.amount', item_template).html('1');
        $('.description', item_template).html('Apekool met Larie');
        $('.price', item_template).html('€ 2,00');

        $('.order-item-wrapper', template).append(item_template);
    }


    $('.order-wrapper').append(template);
}

fetchData();

$(function(){setInterval(time_tick, 1000);});
$(function(){setInterval(fetchData, 10000);});
$(".order-line.expanded").hide();
$("img.3bars").click(barsclick);