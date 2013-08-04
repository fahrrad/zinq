/**
 * Created with PyCharm.
 * User: ward
 * Date: 8/4/13
 * Time: 2:02 PM
 * To change this template use File | Settings | File Templates.
 */


function delete_order(this_button){
    var order_id = $(this_button).closest("div").find("div.id").text()
    $.ajax({
        url: "/rest/orders/delete/" + order_id + "/",
        type: "GET"
     }).done(function(){
            $(this_button).closest("div").hide()
        });

    return false;
};

$(document).ready(function(){
    $("button.delete").click(function(){return delete_order(this, 1);});
})