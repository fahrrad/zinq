$(".order-line.expanded").hide();

function log(text) {

}

function time_tick() {
    if (window.console && window.console.log) {
        console.log("Timetick!");
    }

    $(".order-line-wrapper").each(function () {
            $(this).data("seconds", $(this).data("seconds") + 1);
            $(this).find(".time").html(seconds_to_minutes($(this).data("seconds")));
            $(this).css("background-color", seconds_to_color($(this).data("seconds")));
        }
    )


}

function paddy(n, p, c) {
    var pad_char = typeof c !== 'undefined' ? c : '0';
    var pad = new Array(1 + p).join(pad_char);
    return (pad + n).slice(-pad.length);
}

function seconds_to_minutes(seconds){
    minutes = Math.floor(seconds / 60);
    minutes += ':'
    secs = (seconds % 60);
    minutes += paddy(secs, 2);

    return minutes;
}

function seconds_to_color(seconds){
    //var color = "hsla(" +seconds % 360 +", " +(seconds * 3) % 100 +"%, " +"100%, " +"1.0)";
    var color = "rgb(" + Math.min(255,(seconds * 7) % 255) + ",0,0)";
    if (window.console && window.console.log) {
        console.log(color);
    }
    return color;

}


$("img.3bars").click(function () {
    var order_line_wrapper = $(this).closest(".order-line-wrapper");

    // Show all summaries excelpt this one
    $(".order-line.summary").slideDown();
    $(order_line_wrapper).find(".summary").slideUp();

    // Hide all expanded except this one
    $(".order-line.expanded").slideUp();
    $(order_line_wrapper).find(".expanded").slideDown()
});

$("button.cancel_button").click(function () {
    alert("Cancel");
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
        if (window.console && window.console.log) {
            console.log("Something went south...");
        }
    });
});

$(function(){setInterval(time_tick, 1000);});