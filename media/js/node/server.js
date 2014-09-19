'use strict';

//
// Require all dependencies.
//
// Argh is an light weight argument parser that we use in this example to change
// between parsers and transformers. The following CLI arguments are accepted:
//
// --transformer <value>  (the name of the transformer we want to use)
// --parser <value>       (the name of the parser we want to use)
// --port <value>         (the port number we want to listen to)
//
var argh = require('argh').argv
    , Primus
    , server
    , primus;

//
// Default to the repository, but when we're deployed on a server use the latest
// Primus instance.
//
try {
    Primus = require('../../');
}
catch (e) {
    Primus = require('primus');
}

//
// Some build in Node.js modules that we need:
//
var http = require('http')
    , fs = require('fs');

var pendingOrders = {};
var connectedClients = {};

function contains(array, key) {
    for (var i = 0; i < array.length; i++) {
        if (array[i] == key) {
            return true;
        }
    }
    return false;
}


//
// Create a basic server that will send the compiled library or a basic HTML
// file which we can use for testing.
//
server = http.createServer(function server(req, res) {
    res.setHeader('Content-Type', 'text/html');
    fs.createReadStream(
            __dirname + (~req.url.indexOf('primus.js') ? '/primus.js' : '/order.html')
    ).pipe(res);
});

//
// Now that we've setup our basic server, we can setup our Primus server.
//
primus = new Primus(server, {
    transformer: argh.transformer || 'engine.io',
    pathname: argh.pathname || '/primusexample',
    parser: argh.parser
});

//
// Listen for new connections and send data
//
primus.on('connection', function connection(spark) {
    console.log('Connection NEW ' + spark.id);

    spark.on('data', function data(packet) {
        console.log('incoming:', packet);
        //
        // Close the connection.
        //
        if (packet === 'end') spark.end();

        if (packet.orderId) {
            console.log('Adding ' + spark.id + ' to client list for order ' + packet.orderId);
            if (!(packet.orderId in pendingOrders)) {
                console.log('Adding connection for new order');
                pendingOrders[packet.orderId] = {};
                pendingOrders[packet.orderId][spark.id] = spark;
                connectedClients[spark.id] = packet.orderId;
            } else {
                if (contains(Object.keys(pendingOrders[packet.orderId]), spark.id)) {
                    console.log('Connection already exists for order');
                } else {
                    console.log('Adding connection to existing order');
                    pendingOrders[packet.orderId][spark.id] = spark;
                    connectedClients[spark.id] = packet.orderId;
                }
            }
            console.log("Number of client listening: " + Object.keys(pendingOrders[packet.orderId]).length);
        }

        if (packet.orderDone) {
            console.log('Order done: ' + packet.orderDone);
            var orderIds = Object.keys(pendingOrders);
            if (contains(orderIds, packet.orderDone)) {
                console.log("Number of client listening: " + Object.keys(pendingOrders[packet.orderDone]).length);
                var clientIds = Object.keys(pendingOrders[packet.orderDone]);
                for (var index = 0; index < clientIds.length; index++) {
                    console.log("Sending to: " + pendingOrders[packet.orderDone][clientIds[index]].id);
                    pendingOrders[packet.orderDone][clientIds[index]].write("Order done: " + packet.orderDone);
                    console.log("Delete client: " + pendingOrders[packet.orderDone][clientIds[index]].id);
                    delete connectedClients[clientIds[index]];
                }
                console.log("Delete order: " + packet.orderDone);
                delete pendingOrders[packet.orderDone];
            } else {
                console.log("No pending orders for " + packet.orderId);
            }
        }

        //
        // Echo the responses.
        //
        if (packet.echo) spark.write(packet.echo);

        //
        // Pipe in some data.
        //
        if (packet.pipe) fs.createReadStream(__dirname + '/order.html').pipe(spark, {
            end: false
        });

    });
});

primus.on('disconnection', function connection(spark) {
    console.log('Connection CLOSE ' + spark.id);
    if (contains(Object.keys(connectedClients), spark.id)) {
        console.log("Order pending for client: " + spark.id + " - connectedClients: " + Object.keys(connectedClients).length);
        delete connectedClients[spark.id];
        console.log("Deleted client: " + spark.id + " - connectedClients: " + Object.keys(connectedClients).length);

        var orderIds = Object.keys(pendingOrders);
        for (var index = 0; index < orderIds.length; index++) {
            console.log("Running over orders, orderId:" + orderIds[index]);
            if (contains(Object.keys(pendingOrders[orderIds[index]]), spark.id)) {
                console.log("Deleting client " + spark.id + " for order " + orderIds[index]);
                delete pendingOrders[orderIds[index]][spark.id];
            } else {
                console.log("No order to delete for client " + spark.id);
            }

            //No more clients are listening for this order, remove the order from the pending orders
            if (Object.keys(pendingOrders[orderIds[index]]).length == 0) {
                console.log("No clients listening for order " + orderIds[index] + " deleting order...");
                delete pendingOrders[orderIds[index]];
                console.log("Number of pending orders: " + Object.keys(pendingOrders).length)
            } else {
                console.log("Not removing pending order " + orderIds[index] + " still " + Object.keys(pendingOrders[orderIds[index]]).length + " clients waiting for order confirmation");
            }
        }
    } else {
        console.log("No pending orders for client " + spark.id);
    }
});
//
// Save the compiled file to the hard disk so it can also be distributed over
// cdn's or just be served by something else than the build-in path.
//
primus.save('primus.js');

//
// Everything is ready, listen to a port number to start the server.
//
server.listen(+argh.port || 8080);
