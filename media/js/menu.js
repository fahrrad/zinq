function add_one_of_item(item_pk, order) {
    if (order[item_pk] != undefined) {
        order[item_pk]++;
    } else {
        order[item_pk] = 1;
    }

    return order;
}


function decr_one_of_item(item_pk, order) {
    if (order[item_pk] != undefined && order[item_pk] > 0) {
        order[item_pk]--;
    }

    // Item was reduced to 0 => delete!
    if (order[item_pk] == 0) {
        delete order[item_pk];
    }


    return order;
}


$(document).ready(function () {

    var order = {},
        itemsTotal = 0,
        totalAmount = 0;

    $('h2').click(function () {

        $('.product').slideUp('fast');
        if ($(this).data('clicked') == 'false') {
            $(this).nextUntil('h2').slideUp('fast');
            $(this).data('clicked', 'true');
        } else {
            $(this).nextUntil('h2').slideDown('fast');
            $('h2').data('clicked', 'true');
            $(this).data('clicked', 'false');
        }

        return false;
    });

    $('.product-top').click(function () {

        $('.product-bottom').slideUp('fast');
        if ($(this).data('clicked') == 'false') {
            $('.product-bottom', $(this).parents('.product:first')).slideUp('fast');
            $(this).data('clicked', 'true');
        } else {
            $('.product-bottom', $(this).parents('.product:first')).slideDown('fast');
            $('.product-top').data('clicked', 'true');
            $(this).data('clicked', 'false');
        }

    });


    $('.min').click(function (event) {
        event.preventDefault();

        var amountWrapper = $('.amount', $(this).parents('.amount-wrapper:first')),
            price = parseFloat($('.price', $(this).parents('.product:first')).data('price')),
            item_pk = parseInt($(this).parents('.product:first').data('id')),
            amount = parseInt(amountWrapper.html());

        if (amount >= 1) {
            amount -= 1;
            order = decr_one_of_item(item_pk, order);

            amountWrapper.html(amount);

            totalAmount = parseFloat(totalAmount) - price;
            itemsTotal = itemsTotal - 1;
            displayItemsTotal();
        }

        return false;
    });

    $('.plus').click(function (event) {
        event.preventDefault();

        var amountWrapper = $('.amount', $(this).parents('.amount-wrapper:first')),
            price = parseFloat($('.price', $(this).parents('.product:first')).data('price')),
            item_pk = parseInt($(this).parents('.product:first').data('id')),
            amount = parseInt(amountWrapper.html());

        amount = checkPositive(amount + 1);
        amountWrapper.html(amount);
        order = add_one_of_item(item_pk, order);

        totalAmount = parseFloat(totalAmount) + price;

        itemsTotal = checkPositive(itemsTotal + 1);
        displayItemsTotal();

        return false;
    });

    $('#order').click(function () {

        $.each(order, function (item, amount) {
            console.log(amount, "of", item);
        });
        $('#product-overview').fadeOut(500);
        $('#basket-overview').delay(500).fadeIn(500);

        return false;
    });

    $('#back').click(function () {

        $('#basket-overview').fadeOut(500);
        $('#product-overview').delay(500).fadeIn(500);

        return false;
    });

    $('#confirm').one("click", function () {
        function install_demo_timer() {
            window.setInterval(function(){console.log("installing demo tiner"); window.location.href="/orders/1";}, 5000);
        }

        if ($('#demo_menu').html() == "True"){
            install_demo_timer();
        }

        $.post('/order/p/' + $('#table_uuid').text() + '/', order, function (data) {
            window.location.href = "/wait/" + data.order_uuid;
        });
    });

    function checkPositive(amount) {
        var value = parseInt(amount);

        if (value < 0) {
            value = 0;
        }

        return value;
    }

    function displayItemsTotal() {
        $('#items-counter').html(itemsTotal);
        $('#header-items').html(itemsTotal);

        $('#total-amount').html('€ ' + totalAmount.toFixed(2).replace('.', ','));

        if (itemsTotal > 0) {
            $('#order').show();
        } else {
            $('#order').hide();
        }
    }
});