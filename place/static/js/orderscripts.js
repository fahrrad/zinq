/**
 * Created with PyCharm.
 * User: ward
 * Date: 8/4/13
 * Time: 2:02 PM
 * To change this template use File | Settings | File Templates.
 */


function delete_order(this_button, order_id){
    $.ajax({
        url: "/rest/orders/" + order_id,
        type: "DELETE"
     }).done(function(){
            this_button.closest("tr").hide()
        });
};

$(document).ready(function(){
    $("button.delete").click(function(){return delete_order(this);});
})