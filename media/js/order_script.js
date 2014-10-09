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
            $(this).css("background-color",
                seconds_to_color(
                    $(this).data("seconds")));
        }
    )
}

function paddy(n, p, c) {
    var pad_char = typeof c === 'undefined' ? '0' : c;
    var pad = new Array(1 + p).join(pad_char);
    return (pad + n).slice(-pad.length);
}

function seconds_to_minutes(seconds) {
    var minutes = Math.floor(seconds / 60);
    minutes += ':';
    var secs = (seconds % 60);
    minutes += paddy(secs, 2);

    return minutes;
}

function seconds_to_color(seconds) {
    //var color = "hsla(" +seconds % 360 +", " +(seconds * 3) % 100 +"%, " +"100%, " +"1.0)";
    var color = "rgb(" + Math.min(255, (seconds * 7)) + ",0,0)";
    log(color);

    return color;
}

function barsclick() {
    var order_line_wrapper = $(this).closest(".order-line-wrapper");

    // Hide all expanded except this one
    $(".order-line.expanded").slideUp();
    $(order_line_wrapper).find(".expanded").slideDown();

    // disable this button, to avoid opening and closing of an open orderitem
    $("img.3bars").off("click").click(barsclick);
    $(order_line_wrapper).find("img.3bars").off("click");
}

function addOrder(order) {
    var template = $('#template.order-line-wrapper').clone(true);
    var total = 0.0;

    template.removeAttr('id');
    $('.table', template).html('99');
    template.attr('uuid', order.pk);
    $(template).data('seconds', 0);
    $(template).data('uuid', order.pk);

    $.each(order.item_amounts, function (i, item_amount_price) {
        item_template = $('#template.order-item', template).clone(true);

        item_template.removeAttr('id');

        item = item_amount_price[0]
        amount = item_amount_price[1]
        price = "€ " + item_amount_price[2]

        log(i);
        log("item: " + item);
        log("amount: " + amount);
        log("price: " + price);

        $('.amount', item_template).html(amount);
        $('.description', item_template).html(item);
        $('.price', item_template).html(price);

        total += parseFloat(item_amount_price[2]);

        $('.order-item-wrapper', template).append(item_template);
        item_template.show()
    });

    template.find('.order-line .total').html('totaal € ' + total);

    $('.order-wrapper').append(template);


    $(template).find(".expanded").hide();
    template.show();
}

function fetchData() {
    $.ajax({
        url: "/order/o/" + 1 + "/",
        dataType: "json"
    }).done(function (orders) {
        $.each(orders, function (i, order) {
            if (!$("[uuid='" + order.pk + "']").length) {
                addOrder(order)
            }
        })
    })
}

$(function () {
    $("img.3bars").click(barsclick);

    $("button.cancel_button").click(function () {
        var order_uuid = $(this).closest(".order-line-wrapper").attr("uuid");
        $(this).closest(".order-line-wrapper").slideUp(500);

        var request = $.ajax({
            url: "/order/x/" + order_uuid + "/",
            context: $(this).closest(".order-line-wrapper")
        });
        request.done(function () {
            $(this).closest(".order-line-wrapper").remove();
        });

        log("order " + order_uuid + " done");
    });

    $("button.ready_button").click(function () {
        var order_uuid = $(this).closest(".order-line-wrapper").attr("uuid");
        $(this).closest(".order-line-wrapper").slideUp(500);

        var request = $.ajax({
            url: "/order/d/" + order_uuid + "/",
            context: $(this).closest(".order-line-wrapper")
        });
        request.done(function () {
            $(this).closest(".order-line-wrapper").remove();
        });

        log("order " + order_uuid + " done");
    });

    function set_order_status(order, status) {
        var order_uuid = order.closest(".order-line-wrapper").attr("uuid");

        var endpoint;
        if (status == 'done') {
            endpoint = "/order/d/"
        } else {
            endpoint = "/order/x/"
        }


        order.closest(".order-line-wrapper").slideUp(500);

        var request = $.ajax({
            url: endpoint + order_uuid + "/",
            context: order.closest(".order-line-wrapper")
        });
        request.done(function () {
            order.closest(".order-line-wrapper").remove();
        });

        log("order " + order_uuid + " done");
    }

    fetchData();
    $(function () {
        setInterval(fetchData, 1000);
    });

    $(function () {
        setInterval(time_tick, 1000);
    });
});