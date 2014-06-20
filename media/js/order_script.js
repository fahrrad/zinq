$(".order-line.expanded").hide();

$("img.3bars").click(function(){
    var order_line_wrapper = $(this).closest(".order-line-wrapper");

    // Show all summaries excelpt this one
    $(".order-line.summary").slideDown();
    $(order_line_wrapper).find(".summary").slideUp();

    // Hide all expanded except this one
    $(".order-line.expanded").slideUp();
    $(order_line_wrapper).find(".expanded").slideDown()
});

$("button.cancel_button").click(function(){
    alert("Cancel");
});

$("button.ready_button").click(function(){
    var wrapper = $(this).closest(".order-line-wrapper");
    var order_uuid = $(wrapper).data("uuid");
    $.ajax({
        url: "/orders/d/" + order_uuid + "/",
        type: "GET"
     }).done(function(){
         wrapper.slideUp(400,function() {
            wrapper.remove();
         });

     }).error(function() {
        if ( window.console && window.console.log ) {
            console.log("Something went south...");
        }
    });
});