/**
 * Created with PyCharm.
 * User: ward
 * Date: 8/2/13
 * Time: 7:56 PM
 * To change this template use File | Settings | File Templates.
 */


// Add 1 to the amount textbox under the same tablerow as the button that was just clicked
function add_button(button){
    var input = $(button).closest("tr").find("input.amount");
    var old_val = parseInt(input.val());

    input.val(old_val+1);


    return false;
}


// subtract 1 from the amount textbox under the same tablerow as the button that was just clicked
function decr_button(button){
    var input = $(button).closest("tr").find("input.amount");
    var old_val = parseInt(input.val());
    var new_val = old_val > 0 ? old_val - 1 : old_val;

    input.val(new_val);


    return false;
}

$(document).ready(function(){
    // Bind + and - buttons
    $(".add_button").click(function(){return add_button(this); });
    $(".decr_button").click(function(){return decr_button(this); });
});

