$(function() {

    var socket;

    var connected = function() {
        console.log('Conected');
    };

    var disconnected = function() {
        location = '/';
    };


    var messaged = function(data) {
        console.log(data);
        $('#code_area').val(data['code']);
    };

    setInterval(function(){
        console.log('Sent:');
        socket.send({code: $('#code_area').val() });
    },333);

    var start = function() {
        socket = new io.Socket();
        socket.connect();
        socket.on('connect', connected);
        socket.on('disconnect', disconnected);
        socket.on('message', messaged);
    };

    start();

});
