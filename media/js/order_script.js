$(".order-line.expanded").hide();

$("img.3bars").click(function(){
    var order_line_wrapper = $(this).closest(".order-line-wrapper");

    // Show all summaries excelpt this one
    $(".order-line.summary").show();
    $(order_line_wrapper).find(".summary").hide();

    // Hide all expanded except this one
    $(".order-line.expanded").hide();
    $(order_line_wrapper).find(".expanded").show()
});

$("button.cancel_button").click(function(){
    alert("Cancel");
})