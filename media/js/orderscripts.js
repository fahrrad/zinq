/**
 * Created with PyCharm.
 * User: ward
 * Date: 8/4/13
 * Time: 2:02 PM
 * To change this template use File | Settings | File Templates.
 */


// the timer for refreshing the orders
var timer;
var path_name;


function delete_order(this_button){
    var order_uuid = $(this_button).closest("div").find("div.id").text()
    $.ajax({
        url: "/rest/orders/delete/" + order_uuid + "/",
        type: "GET"
     }).done(function(){
            $(this_button).closest("div").slideUp();
     });

    return false;
};

// Loads the current orders from the server
function refresh(){
    $.ajax({
        url: path_name,
        dataType: "json"
    }).done(function(data){

        window.clearInterval(timer);
        
        // This div is on the body level
        var uber_div = document.createElement('div');
        // |-------------------------------------------
        // | interval  = 2000
        // | orders: |---------------------------------
        // |         | pk : |--------------------------
        // |         |      | tableNr
        // |         |      | item_amounts:|-----------
        // |         |      |              | (name, amount)
        // |         |      |              | (name, amount) 
        // |         |      |              |-----------
        // |         |      |--------------------------
        // |         |      
        // |         | pk : |--------------------------
        // |         |      | tableNr
        // |         |      | item_amounts:|-----------
        // |         |      |              | (name, amount)
        // |         |      |              | (name, amount) 
        // |         |      |              |-----------
        // |         |      |--------------------------
        // |         |---------------------------------   
        // |-------------------------------------------


            // Loop over every order
            for(var item in data.orders)
            {
                // this div will be placed in the Uber diff
                var div = document.createElement('div');
                div.setAttribute("class", "order");
                var order_data = data.orders[item];
                
                // This div will be used by the delete button to sent backt the Id of the 
                // thing to end. It should be hidden.
                var id_text = document.createElement("div");
                id_text.setAttribute("class", "id");
                id_text.innerHTML = item;
                div.appendChild(id_text);

                // Add the table number
                var tableNr_div = document.createElement("div");
                var tableNr = data.orders[item].table_nr;
                tableNr_div.innerHTML = "Table " + tableNr;
                div.appendChild(tableNr_div);

                // This list will contain the amount and names of the order
                // items
                var list = document.createElement('ul')
                div.appendChild(list);

                // JSON part that contains the amounts + names for this 
                var item_amounts = data.orders[item].item_amounts

                // Loop over the amounts and items for each order
                for(var key in item_amounts){
                    var item_amount = item_amounts[key]
                    var item = item_amount[0];
                    var amount = item_amount[1];
                    
                    var li_el = document.createElement('li');
                    li_el.innerHTML = "<span class=\"amount\"> " + amount 
                        + "</span> <span class=\"item\"> " + item + " </span>";
                    list.appendChild(li_el);
                }

                // Adds the button to delete the order
                var delete_button = document.createElement('button');
                var button_text = document.createTextNode('delete');
                delete_button.appendChild(button_text);

                delete_button.setAttribute('onclick', 'delete_order(this)');
                delete_button.setAttribute('class', 'delete');

                div.appendChild(delete_button);
                uber_div.appendChild(div);
            }


            $('.orders').html(uber_div);
            timer = window.setInterval(refresh, data.interval);
        }
    );
}

$(document).ready(function(){
    path_name = window.location.pathname;
    $("button.delete").click(function(){return delete_order(this);});
    timer = window.setInterval(refresh, 2000)
})